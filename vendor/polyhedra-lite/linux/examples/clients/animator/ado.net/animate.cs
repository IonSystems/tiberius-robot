//
// Polyhedra ADO.NET Data Provider Active Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// This sample illustrates updating through an active query using the
// Polyhedra ADO.NET data provider.
// 
// It periodically changes the content of the currency table in the database.

//-----------------------------------------------------------------------------
// NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
// demonstrate one or more features of the Polyhedra product.
// It may well need adaption for use in a live installation, and
// Enea Software AB and its agents and distributors do not warrant this code.
//-----------------------------------------------------------------------------

using Polyhedra.Data.PolyClient;
using System;
using System.Data;
using System.Data.Common;
using System.Threading;

namespace Polyhedra.Data.PolySample
{
	public class PolyAnimate
	{
		private static AutoResetEvent WaitHandle = new AutoResetEvent(false);

		public static void Main(string[] args)
		{
			PolyAnimate polyAnimate = new PolyAnimate();

			polyAnimate.Run(args);
		}

		private void Run(string[] args)
		{
			string service = "8001";
			bool ftEnable = false;

			// Check the correct number of arguments have been supplied
			if (args.Length > 2)
			{
				Console.WriteLine("usage: {0} [<data service> [FT]]", System.AppDomain.CurrentDomain.FriendlyName);
				return;
			}

			// Check whether a service argument has been supplied
			if (args.Length >= 1)
			{
				service = args[0];
			}

			// Check wether an FT argument has been supplied
			if (args.Length >= 2)
			{
				ftEnable = args[1].Equals("FT");
			}

			// Build a connection string and connect to the database
			PolyConnectionStringBuilder builder = new PolyConnectionStringBuilder();

			builder.Service = service;

			// Set FT connection settings
			builder.FTEnable = ftEnable;
			builder.FTHeartbeatInterval = 1000;
			builder.FTHeartbeatTimeout = 1000;
			builder.FTReconnectionCount = 1000;
			builder.FTReconnectionInterval = 1000;
			builder.FTReconnectionTimeout = 1000;

			PolyConnection connection = new PolyConnection(builder.ConnectionString);

			// Register for state change events on the connection
			// This is used to detect loss of connection to the database
			connection.StateChange += OnStateChange;

			// Register for FT mode change events on the connection
			connection.FTModeChange += OnFTModeChange;

			Console.WriteLine("Connecting to {0}{1}...", service, ftEnable ? " Fault Tolerant" : "");

			try
			{
				connection.Open();
			}
			catch (Exception)
			{
				Console.WriteLine("Failed to connect to database");
				return;
			}

			Console.WriteLine("Connection made successfully.");

			// Create an active data adapter to perform the active query
			PolyActiveDataAdapter adapter = new PolyActiveDataAdapter("select code,usdollar from currency", connection);

			// Primary key information must be added to the data table
			adapter.MissingSchemaAction = MissingSchemaAction.AddWithKey;

			// Create a data table to hold the result
			DataSet dataSet = new DataSet();

			DataTable dataTable = dataSet.Tables.Add("currency");

			// Add a column to record the starting usdollar value
			DataColumn dataColumn = dataTable.Columns.Add("usdollar_starting", typeof(double));

			dataColumn.DefaultValue = 0.0;

			// Add a column to record the last change made to the currency
			dataColumn = dataTable.Columns.Add("change", typeof(double));

			dataColumn.DefaultValue = 0.0;

			// Perform an initial fill of the data table
			adapter.Fill(dataSet, "currency");

			// Change the results of the initial fill
			ChangeData(dataTable, adapter);

			// Register for data change events
			// This indicates when a delta is available for the active query
			adapter.DataChange += OnDataChange;

			while (true)
			{
				if (WaitHandle.WaitOne(2000))
				{
					// Stop when connection to the database is lost
					if (connection.State == ConnectionState.Closed)
					{
						break;
					}

					// Apply the delta to the data table
					adapter.FillDelta(dataTable);
				}
				else
				{
					ChangeData(dataTable, adapter);
				}
			}

			connection.Close();
		}

		private void ChangeData(DataTable dataTable, PolyActiveDataAdapter adapter)
		{
			Console.WriteLine("Start update through active query");

			// Apply changes to the data table in a single transaction
			PolyTransaction transaction;

			try
			{
				transaction = adapter.SelectCommand.Connection.BeginTransaction();

				adapter.SelectCommand.Transaction = transaction;
			}
			catch (Exception e)
			{
				Console.WriteLine("BeginTransaction failure");
				WriteException(e);
				return;
			}

			foreach (DataRow dataRow in dataTable.Rows)
			{
				double usdollar_starting = (double)dataRow["usdollar_starting"];
				string code = (string)dataRow["code"];
				double usdollar = (double)dataRow["usdollar"];
				double change = (double)dataRow["change"];

				// Work out the change we want to make
				if (change == 0)
				{
					usdollar_starting = usdollar;
					change = usdollar * 0.01;

					dataRow["usdollar_starting"] = usdollar_starting;
				}

				if (change > 0)
				{
					if (usdollar + change > usdollar_starting * 1.1)
					{
						Console.WriteLine("Upper limit crossed");
						change = -change;
					}
				}
				else
				{
					if (usdollar + change <= usdollar_starting * 0.9)
					{
						Console.WriteLine("Lower limit crossed");
						change = -change;
					}
				}

				usdollar += change;

				Console.WriteLine("Change usdollar field of {0} by {1:F6} to {2:F6}", code, change, usdollar);

				dataRow["usdollar"] = usdollar;
				dataRow["change"] = change;
			}

			// If the table is not empty, commit the changes we have just set up
			if (dataTable.Rows.Count > 0)
			{
				try
				{
					adapter.Update(dataTable);

					transaction.Commit();
					Console.WriteLine("Transaction complete");
				}
				catch (Exception e)
				{
					Console.WriteLine("Commit failure");
					WriteException(e);
				}
			}
		}

		private void WriteException(Exception exception)
		{
			// Display the content of an exception
			if (exception is System.AggregateException)
			{
				foreach (Exception innerException in ((System.AggregateException)exception).InnerExceptions)
				{
					WriteException(innerException);
				}
			}
			else if (exception is PolyException)
			{
				// Display the details of all Polyhedra errors
				foreach (PolyError error in ((PolyException)exception).Errors)
				{
					Console.WriteLine("{0:X8}: {1}", error.Code, error.Message);
				}
			}
			else
			{
				Console.WriteLine("Exception: {0}", exception.Message);
			}
		}

		private static void OnStateChange(object sender, StateChangeEventArgs args)
		{
			// If the connection is closed, wake-up the main thread
			PolyConnection connection = (PolyConnection)sender;

			if (connection.State == ConnectionState.Closed)
			{
				WaitHandle.Set();
			}
		}

		private static void OnFTModeChange(object sender, PolyFTModeChangeEventArgs args)
		{
			// Display the new FT mode
			PolyConnection connection = (PolyConnection)sender;

			Console.WriteLine("Connection: {0}, mode: {1}", connection.DataSource, connection.FTMode);
		}

		private static void OnDataChange(object sender, PolyDataChangeEventArgs args)
		{
			// A delta is available so wake-up the main thread
			WaitHandle.Set();
		}
	}
}

// End of file