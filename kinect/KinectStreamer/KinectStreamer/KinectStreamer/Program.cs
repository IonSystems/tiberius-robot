using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace KinectStreamer
{

    using Microsoft.Kinect;
    using System.Drawing;
    using System.IO;
    using System.Windows.Media.Imaging;
    using System.Drawing.Imaging;
    using System.Windows.Media;
    using System.Windows;
    using System.Threading;
    using System.Security.Principal;
    class Streamer
    {


        /// <summary>
        /// Active Kinect sensor
        /// </summary>
        private KinectSensor kinectSensor = null;

        /// <summary>
        /// Reader for color frames
        /// </summary>
        private ColorFrameReader colorFrameReader = null;
        private InfraredFrameReader infraredFrameReader = null;

        private FrameDescription infraredFrameDescription = null;
        /// <summary>
        /// Bitmap to display
        /// </summary>
        private WriteableBitmap colorBitmap = null;
        private WriteableBitmap infraredBitmap = null;
        private WriteableBitmap tempInfraredBitmap = null;
        private WriteableBitmap tempColorBitmap = null;
        /// <summary>
        /// Maximum value (as a float) that can be returned by the InfraredFrame
        /// </summary>
        private const float InfraredSourceValueMaximum = (float)ushort.MaxValue;

        /// <summary>
        /// The value by which the infrared source data will be scaled
        /// </summary>
        private const float InfraredSourceScale = 0.75f;

        /// <summary>
        /// Smallest value to display when the infrared data is normalized
        /// </summary>
        private const float InfraredOutputValueMinimum = 0.01f;

        /// <summary>
        /// Largest value to display when the infrared data is normalized
        /// </summary>
        private const float InfraredOutputValueMaximum = 1.0f;

        /// <summary>
        /// Current status text to display
        /// </summary>
        private string statusText = null;
        public string path = "C:\\inetpub\\wwwroot\\colour.jpg";
        public string irpath = "C:\\inetpub\\wwwroot\\ir.jpg";
        private int counter = 0;

        /// <summary>
        /// Initializes a new instance of the Streamer class.
        /// </summary>
        /// 
        public Streamer()
        {
            this.kinectSensor = KinectSensor.GetDefault();

            // open the reader for the color frames
            this.colorFrameReader = this.kinectSensor.ColorFrameSource.OpenReader();
            this.infraredFrameReader = this.kinectSensor.InfraredFrameSource.OpenReader();


            // wire handler for frame arrival
            this.colorFrameReader.FrameArrived += this.Reader_ColorFrameArrived;
            this.infraredFrameReader.FrameArrived += this.Reader_InfraredFrameArrived;


            // create the colorFrameDescription from the ColorFrameSource using Bgra format
            FrameDescription colorFrameDescription = this.kinectSensor.ColorFrameSource.CreateFrameDescription(ColorImageFormat.Bgra);
            this.infraredFrameDescription = this.kinectSensor.InfraredFrameSource.FrameDescription;

            // create the bitmap to display
            this.colorBitmap = new WriteableBitmap(colorFrameDescription.Width, colorFrameDescription.Height, 96.0, 96.0, PixelFormats.Bgr32, null);
            this.infraredBitmap = new WriteableBitmap(this.infraredFrameDescription.Width, this.infraredFrameDescription.Height, 96.0, 96.0, PixelFormats.Gray32Float, null);


            // open the sensor
            this.kinectSensor.Open();

            
        }
        private Bitmap BitmapFromWriteableBitmap(WriteableBitmap writeBmp)
        {
            System.Drawing.Bitmap bmp;
            using (MemoryStream outStream = new MemoryStream())
            {
                BitmapEncoder enc = new BmpBitmapEncoder();
                enc.Frames.Add(BitmapFrame.Create(writeBmp));
                enc.Save(outStream);
                System.Drawing.Size size = new System.Drawing.Size(640, 360);
                bmp = new Bitmap(outStream);
                bmp = new Bitmap(bmp, size);
                outStream.Close();
            }
            return bmp;
        }

        private void SaveImage()
        {
           
            if (this.colorBitmap != null && counter++ > 2)
            {
                counter = 0;



                ImageCodecInfo myImageCodecInfo;
                Encoder myEncoder;
                EncoderParameter myEncoderParameter;
                EncoderParameters myEncoderParameters;

                // Create a Bitmap object based on a BMP file.


                // Get an ImageCodecInfo object that represents the JPEG codec.
                myImageCodecInfo = GetEncoderInfo("image/jpeg");

                // Create an Encoder object based on the GUID

                // for the Quality parameter category.
                myEncoder = Encoder.Quality;

                // Create an EncoderParameters object.

                // An EncoderParameters object has an array of EncoderParameter

                // objects. In this case, there is only one

                // EncoderParameter object in the array.
                myEncoderParameters = new EncoderParameters(1);

                // Save the bitmap as a JPEG file with quality level 25.
                myEncoderParameter = new EncoderParameter(myEncoder, 25L);
                myEncoderParameters.Param[0] = myEncoderParameter;







                Bitmap bitmap = BitmapFromWriteableBitmap(this.colorBitmap);
                bitmap.RotateFlip(RotateFlipType.RotateNoneFlipX);




                

                // write the new file to disk
                try
                {
                    bitmap.Save(path, myImageCodecInfo, myEncoderParameters);                    
                }
                catch (IOException)
                {
                    Console.WriteLine("Failed to write screenshot");
                }
            }
            
        }

        private void SaveInfraredImage()
        {

            if (this.infraredBitmap != null && counter++ > 2)
            {
                counter = 0;



                ImageCodecInfo myImageCodecInfo;
                Encoder myEncoder;
                EncoderParameter myEncoderParameter;
                EncoderParameters myEncoderParameters;

                // Create a Bitmap object based on a BMP file.


                // Get an ImageCodecInfo object that represents the JPEG codec.
                myImageCodecInfo = GetEncoderInfo("image/jpeg");

                // Create an Encoder object based on the GUID

                // for the Quality parameter category.
                myEncoder = Encoder.Quality;

                // Create an EncoderParameters object.

                // An EncoderParameters object has an array of EncoderParameter

                // objects. In this case, there is only one

                // EncoderParameter object in the array.
                myEncoderParameters = new EncoderParameters(1);

                // Save the bitmap as a JPEG file with quality level 25.
                myEncoderParameter = new EncoderParameter(myEncoder, 25L);
                myEncoderParameters.Param[0] = myEncoderParameter;
                                
                Bitmap bitmap = BitmapFromWriteableBitmap(this.infraredBitmap);
                bitmap.RotateFlip(RotateFlipType.RotateNoneFlipX);
                
                // write the new file to disk
                try
                {
                    bitmap.Save(path, myImageCodecInfo, myEncoderParameters);
                }
                catch (IOException)
                {
                    Console.WriteLine("Failed to write screenshot");
                }
            }

        }

        private static ImageCodecInfo GetEncoderInfo(String mimeType)
        {
            int j;
            ImageCodecInfo[] encoders;
            encoders = ImageCodecInfo.GetImageEncoders();
            for (j = 0; j < encoders.Length; ++j)
            {
                if (encoders[j].MimeType == mimeType)
                    return encoders[j];
            }
            return null;
        }
        /// <summary>
        /// Handles the color frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_ColorFrameArrived(object sender, ColorFrameArrivedEventArgs e)
        {
            // ColorFrame is IDisposable
            using (ColorFrame colorFrame = e.FrameReference.AcquireFrame())
            {
                if (colorFrame != null)
                {
                    FrameDescription colorFrameDescription = colorFrame.FrameDescription;

                    using (KinectBuffer colorBuffer = colorFrame.LockRawImageBuffer())
                    {

                        this.tempColorBitmap = new WriteableBitmap(colorFrameDescription.Width, colorFrameDescription.Height, 96.0, 96.0, PixelFormats.Bgr32, null);
                        this.tempColorBitmap.Lock();

                        // verify data and write the new color frame data to the display bitmap
                        if ((colorFrameDescription.Width == this.tempColorBitmap.PixelWidth) && (colorFrameDescription.Height == this.tempColorBitmap.PixelHeight))
                            {
                                colorFrame.CopyConvertedFrameDataToIntPtr(
                                    this.tempColorBitmap.BackBuffer,
                                    (uint)(colorFrameDescription.Width * colorFrameDescription.Height * 4),
                                    ColorImageFormat.Bgra);

                                this.tempColorBitmap.AddDirtyRect(new Int32Rect(0, 0, this.tempColorBitmap.PixelWidth, this.tempColorBitmap.PixelHeight));
                            }
                        this.tempColorBitmap.Unlock();
                        if (this.tempColorBitmap.CanFreeze)
                        {
                            this.tempColorBitmap.Freeze();
                            this.colorBitmap = this.tempColorBitmap;
                        }
                        
                        
                    }
                }
            }

            SaveImage();
        }

        /// <summary>
        /// Handles the infrared frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_InfraredFrameArrived(object sender, InfraredFrameArrivedEventArgs e)
        {
            // InfraredFrame is IDisposable
            using (InfraredFrame infraredFrame = e.FrameReference.AcquireFrame())
            {
                if (infraredFrame != null)
                {
                    // the fastest way to process the infrared frame data is to directly access 
                    // the underlying buffer
                    using (Microsoft.Kinect.KinectBuffer infraredBuffer = infraredFrame.LockImageBuffer())
                    {
                        // verify data and write the new infrared frame data to the display bitmap
                        if (((this.infraredFrameDescription.Width * this.infraredFrameDescription.Height) == (infraredBuffer.Size / this.infraredFrameDescription.BytesPerPixel)) &&
                            (this.infraredFrameDescription.Width == this.infraredBitmap.PixelWidth) && (this.infraredFrameDescription.Height == this.infraredBitmap.PixelHeight))
                        {
                            this.ProcessInfraredFrameData(infraredBuffer.UnderlyingBuffer, infraredBuffer.Size);
                        }
                    }
                }
            }
        }

        private unsafe void ProcessInfraredFrameData(IntPtr infraredFrameData, uint infraredFrameDataSize)
        {
            // infrared frame data is a 16 bit value
            ushort* frameData = (ushort*)infraredFrameData;

            this.tempInfraredBitmap = new WriteableBitmap(this.infraredFrameDescription.Width, this.infraredFrameDescription.Height, 96.0, 96.0, PixelFormats.Gray32Float, null);
            // lock the target bitmap
            this.tempInfraredBitmap.Lock();

            // get the pointer to the bitmap's back buffer
            float* backBuffer = (float*)this.tempInfraredBitmap.BackBuffer;

            // process the infrared data
            for (int i = 0; i < (int)(infraredFrameDataSize / this.infraredFrameDescription.BytesPerPixel); ++i)
            {
                // since we are displaying the image as a normalized grey scale image, we need to convert from
                // the ushort data (as provided by the InfraredFrame) to a value from [InfraredOutputValueMinimum, InfraredOutputValueMaximum]
                backBuffer[i] = Math.Min(InfraredOutputValueMaximum, (((float)frameData[i] / InfraredSourceValueMaximum * InfraredSourceScale) * (1.0f - InfraredOutputValueMinimum)) + InfraredOutputValueMinimum);
            }

            // mark the entire bitmap as needing to be drawn
            this.tempInfraredBitmap.AddDirtyRect(new Int32Rect(0, 0, this.infraredBitmap.PixelWidth, this.infraredBitmap.PixelHeight));

            // unlock the bitmap
            this.tempInfraredBitmap.Unlock();

            if (this.tempInfraredBitmap.CanFreeze)
            {
                this.tempInfraredBitmap.Freeze();
                this.infraredBitmap = this.tempInfraredBitmap;
            }

            SaveInfraredImage();
        }

        static void Main(string[] args)
        {
            bool isElevated;
            WindowsIdentity identity = WindowsIdentity.GetCurrent();
            WindowsPrincipal principal = new WindowsPrincipal(identity);
            isElevated = principal.IsInRole(WindowsBuiltInRole.Administrator);

            if (!isElevated)
            {
                Console.WriteLine("Must be run as administrator!");
                Thread.Sleep(5000);
                Environment.Exit(1);
            }


            Console.WriteLine("Starting Kinect Streamer");
            Streamer streamer = new Streamer();
            Console.WriteLine("Saving colour images to: " + streamer.path);

            Console.WriteLine("Press Ctrl+C to exit");
            Console.CancelKeyPress += delegate
            {
                Cleanup(streamer);
            };

            while (true) { Thread.Sleep(1); }

            
        }

        private static void Cleanup(Streamer streamer)
        {
            Console.WriteLine("Cleaning up...");
            if (streamer.colorFrameReader != null)
            {
                // ColorFrameReder is IDisposable
                streamer.colorFrameReader.Dispose();
                streamer.colorFrameReader = null;
            }

            if (streamer.kinectSensor != null)
            {
                streamer.kinectSensor.Close();
                streamer.kinectSensor = null;
            }
            Environment.Exit(0);
        }
    }
}
