//------------------------------------------------------------------------------
// <copyright file="MainWindow.xaml.cs" company="Microsoft">
//     Copyright (c) Microsoft Corporation.  All rights reserved.
// </copyright>
//------------------------------------------------------------------------------

namespace Microsoft.Samples.Kinect.DepthBasics
{
    using System;
    using System.ComponentModel;
    using System.Diagnostics;
    using System.Globalization;
    using System.IO;
    using System.Windows;
    using System.Windows.Media;
    using System.Windows.Media.Imaging;
    using Microsoft.Kinect;
    using System.Collections.Generic;
    /// <summary>
    /// Interaction logic for MainWindow
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        /// <summary>
        /// Map depth range to byte range
        /// </summary>
        private const int MapDepthToByte = 8000 / 256;

        private const int ChunkSize = 8;
        private const int scale = 8;
        private ushort[][][,] chunks = new ushort[ChunkSize][][,];
        private long[,] chunkMean = new long[ChunkSize, ChunkSize];
        private double[,] chunkStandardDeviation = new double[ChunkSize, ChunkSize];

        /// <summary>
        /// Active Kinect sensor
        /// </summary>
        private KinectSensor kinectSensor = null;

        /// <summary>
        /// Reader for depth frames
        /// </summary>
        private DepthFrameReader depthFrameReader = null;

        /// <summary>
        /// Description of the data contained in the depth frame
        /// </summary>
        private FrameDescription depthFrameDescription = null;

        /// <summary>
        /// Bitmap to display
        /// </summary>
        private WriteableBitmap depthBitmap = null;

        /// <summary>
        /// Intermediate storage for frame data converted to color
        /// </summary>
        private byte[] depthPixels = null;
        private ushort[,] depthGrid = null;

        /// <summary>
        /// Current status text to display
        /// </summary>
        private string statusText = null;

        /// <summary>
        /// Initializes a new instance of the MainWindow class.
        /// </summary>
        public MainWindow()
        {




            // get the kinectSensor object
            kinectSensor = KinectSensor.GetDefault();

            // open the reader for the depth frames
            depthFrameReader = kinectSensor.DepthFrameSource.OpenReader();

            // wire handler for frame arrival
            depthFrameReader.FrameArrived += Reader_FrameArrived;

            // get FrameDescription from DepthFrameSource
            depthFrameDescription = kinectSensor.DepthFrameSource.FrameDescription;

            // allocate space to put the pixels being received and converted
            depthPixels = new byte[ChunkSize * scale * ChunkSize * scale];
            depthGrid = new ushort[depthFrameDescription.Width, depthFrameDescription.Height];

            // create the bitmap to display
            depthBitmap = new WriteableBitmap(ChunkSize * scale, ChunkSize * scale, ChunkSize, ChunkSize, PixelFormats.Gray8, null);

            // set IsAvailableChanged event notifier
            kinectSensor.IsAvailableChanged += Sensor_IsAvailableChanged;

            // open the sensor
            kinectSensor.Open();

            // set the status text
            StatusText = kinectSensor.IsAvailable ? Properties.Resources.RunningStatusText
                                                            : Properties.Resources.NoSensorStatusText;

            // use the window object as the view model in this simple example
            DataContext = this;

            // initialize the components (controls) of the window
            InitializeComponent();
        }

        /// <summary>
        /// INotifyPropertyChangedPropertyChanged event to allow window controls to bind to changeable data
        /// </summary>
        public event PropertyChangedEventHandler PropertyChanged;

        /// <summary>
        /// Gets the bitmap to display
        /// </summary>
        public ImageSource ImageSource
        {
            get
            {

                return this.depthBitmap;

            }
        }

        /// <summary>
        /// Gets or sets the current status text to display
        /// </summary>
        public string StatusText
        {
            get
            {
                return this.statusText;
            }

            set
            {
                if (this.statusText != value)
                {
                    this.statusText = value;

                    // notify any bound elements that the text has changed
                    if (this.PropertyChanged != null)
                    {
                        this.PropertyChanged(this, new PropertyChangedEventArgs("StatusText"));
                    }
                }
            }
        }

        /// <summary>
        /// Execute shutdown tasks
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void MainWindow_Closing(object sender, CancelEventArgs e)
        {
            if (this.depthFrameReader != null)
            {
                // DepthFrameReader is IDisposable
                this.depthFrameReader.Dispose();
                this.depthFrameReader = null;
            }

            if (this.kinectSensor != null)
            {
                this.kinectSensor.Close();
                this.kinectSensor = null;
            }
        }

        /// <summary>
        /// Handles the user clicking on the screenshot button
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void ScreenshotButton_Click(object sender, RoutedEventArgs e)
        {
            if (this.depthBitmap != null)
            {
                // create a png bitmap encoder which knows how to save a .png file
                BitmapEncoder encoder = new PngBitmapEncoder();

                // create frame from the writable bitmap and add to encoder
                encoder.Frames.Add(BitmapFrame.Create(this.depthBitmap));

                string time = System.DateTime.UtcNow.ToString("hh'-'mm'-'ss", CultureInfo.CurrentUICulture.DateTimeFormat);

                string myPhotos = Environment.GetFolderPath(Environment.SpecialFolder.MyPictures);

                string path = Path.Combine(myPhotos, "KinectScreenshot-Depth-" + time + ".png");

                // write the new file to disk
                try
                {
                    // FileStream is IDisposable
                    using (FileStream fs = new FileStream(path, FileMode.Create))
                    {
                        encoder.Save(fs);
                    }

                    this.StatusText = string.Format(CultureInfo.CurrentCulture, Properties.Resources.SavedScreenshotStatusTextFormat, path);
                }
                catch (IOException)
                {
                    this.StatusText = string.Format(CultureInfo.CurrentCulture, Properties.Resources.FailedScreenshotStatusTextFormat, path);
                }
            }
        }

        /// <summary>
        /// Handles the depth frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_FrameArrived(object sender, DepthFrameArrivedEventArgs e)
        {
            bool depthFrameProcessed = false;

            using (DepthFrame depthFrame = e.FrameReference.AcquireFrame())
            {
                if (depthFrame != null)
                {
                    // the fastest way to process the body index data is to directly access 
                    // the underlying buffer
                    using (Microsoft.Kinect.KinectBuffer depthBuffer = depthFrame.LockImageBuffer())
                    {
                        // verify data and write the color data to the display bitmap
                        if (((this.depthFrameDescription.Width * this.depthFrameDescription.Height) == (depthBuffer.Size / this.depthFrameDescription.BytesPerPixel)))
                        {
                            // Note: In order to see the full range of depth (including the less reliable far field depth)
                            // we are setting maxDepth to the extreme potential depth threshold
                            ushort maxDepth = ushort.MaxValue;

                            // If you wish to filter by reliable depth distance, uncomment the following line:
                            //// maxDepth = depthFrame.DepthMaxReliableDistance

                            this.ProcessDepthFrameData(depthBuffer.UnderlyingBuffer, depthBuffer.Size, depthFrame.DepthMinReliableDistance, maxDepth);
                            depthFrameProcessed = true;
                        }
                    }
                }
            }

            if (depthFrameProcessed)
            {
                this.RenderDepthPixels();
            }
        }

        /// <summary>
        /// Renders color pixels into the writeableBitmap.
        /// </summary>
        private void RenderDepthPixels()
        {
            this.depthBitmap.WritePixels(
                new Int32Rect(0, 0, ChunkSize * scale, ChunkSize * scale),
                depthPixels,
                depthBitmap.PixelWidth,
                0);

        }

        /// <summary>
        /// Handles the event which the sensor becomes unavailable (E.g. paused, closed, unplugged).
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Sensor_IsAvailableChanged(object sender, IsAvailableChangedEventArgs e)
        {
            // on failure, set the status text
            this.StatusText = this.kinectSensor.IsAvailable ? Properties.Resources.RunningStatusText
                                                            : Properties.Resources.SensorNotAvailableStatusText;
        }

        /// <summary>
        /// Directly accesses the underlying image buffer of the DepthFrame to 
        /// create a displayable bitmap.
        /// This function requires the /unsafe compiler option as we make use of direct
        /// access to the native memory pointed to by the depthFrameData pointer.
        /// </summary>
        /// <param name="depthFrameData">Pointer to the DepthFrame image data</param>
        /// <param name="depthFrameDataSize">Size of the DepthFrame image data</param>
        /// <param name="minDepth">The minimum reliable depth value for the frame</param>
        /// <param name="maxDepth">The maximum reliable depth value for the frame</param>
        private unsafe void ProcessDepthFrameData(IntPtr depthFrameData, uint depthFrameDataSize, ushort minDepth, ushort maxDepth)
        {
            // depth frame data is a 16 bit value
            ushort* frameData = (ushort*)depthFrameData;

            int column = 0;
            int row = 0;

            // convert depth to a visual representation
            for (int i = 0; i < (int)(depthFrameDataSize / this.depthFrameDescription.BytesPerPixel); ++i)
            {
                // Get the depth for this pixel              

                depthGrid[column, row] = (byte)(frameData[i] >= minDepth && frameData[i] <= maxDepth ? (frameData[i]) : 0);

                // Work out which grid position we are in
                column++;
                if (column >= 512)
                {
                    column = 0;
                    row++;
                }

            }
            // Split the data into chunks
            createChunks(depthGrid);


            // Calculate standard deviation on chunks
            int count = 63;

            for (int gridRow = 0; gridRow < ChunkSize; gridRow++)
            {
                for (int gridColumn = 0; gridColumn < ChunkSize; gridColumn++)
                {
                    CalculateStandardDeviation(chunks[gridRow][gridColumn], 512 / ChunkSize, 424 / ChunkSize, out chunkMean[gridRow, gridColumn], out chunkStandardDeviation[gridRow, gridColumn]);

                    // For testing ////////////////////////////
                    //chunkStandardDeviation[column,row] = count-- * 4;    
                    ///////////////////////////////////////////   
                }
            }

            // Put the standard deviations into the display buffer
            int counter = 0;

            for (int gridRow = 0; gridRow < ChunkSize; gridRow++)
            {
                for (int gridColumn = ChunkSize-1; gridColumn >= 0; gridColumn--)
                {
                    ExtractData(counter, gridRow, gridColumn);

                    counter += scale;

                }
                counter -= scale * scale;
                counter += scale * ChunkSize * scale;
            }

        }

        private unsafe void ExtractData(int counter, int gridRow, int gridColumn)
        {
            for (int scaledRow = 0; scaledRow < scale; scaledRow++)
            {
                for (int scaledColumn = 0; scaledColumn < scale; scaledColumn++)
                {
                    this.depthPixels[counter + (ChunkSize * scale * scaledRow) + scaledColumn] = (byte)(chunkStandardDeviation[gridRow, gridColumn] * 20);
                }

            }
        }



        /// <summary>
        /// Splits a grid of data into a number of chunks specified by ChunkSize^2
        /// 
        /// Resulting chunks are stored in 'chunks'
        /// </summary>
        /// <param name="grid">The grid to split up</param>
        private void createChunks(ushort[,] grid)
        {
            


            for (int i = 0; i < ChunkSize; i++)
            {
                chunks[i] = new ushort[ChunkSize][,];
                for (int j = 0; j < ChunkSize; j++)
                {
                    chunks[i][j] = new ushort[512 / ChunkSize, 424 / ChunkSize];
                }
            }


            for(int i = 1; i < 100; i++)
            {
                if(512 % i == 0)
                {
                    Console.WriteLine("divisable by: " + i);
                }
            }

            for (int row = 0; row < 424; row++)
            {
                for (int column = 0; column < 512; column++)
                {
                    chunks[row / 53][column / 64][column % 64, row % 53] = grid[column, row];
                }
            }



        }












        /// <summary>
        /// Calculate standard deviation and mean of a grid
        /// </summary>
        /// <param name="grid">The grid to use</param>
        /// <param name="width">The width of the grid</param>
        /// <param name="height">The height of the grid</param>
        /// <param name="mean">The calculated mean from the grid</param>
        /// <param name="standardDeviation">The calculated standard deviation from the grid</param>
        private void CalculateStandardDeviation(ushort[,] grid, int width, int height, out long mean, out double standardDeviation)
        {
            int n = 0;
            long sum = 0;
            long vsum = 0;

            for (int column = 0; column < width; column++)
            {
                for (int row = 0; row < height; row++)
                {

                    if (grid[column, row] != 0)
                    {
                    sum += grid[column, row];
                    vsum += (grid[column, row] * grid[column, row]);
                     n++;
                    }

                }
            }
            mean = 0;
            standardDeviation = 0;
            if (n > 0)
            {
                mean = (sum / n);
                long variance = vsum / n;
                standardDeviation = Math.Sqrt(variance / n);
            }



        }
    }
}
