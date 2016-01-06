//
// Polyhedra ADO.NET Data Provider Persist Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// This sample takes a single parameter, being the maximum size of the file.
// It launches an active query on journalcontrol - which holds the size of the
// load_file. When the load_file crosses the the size boundary, then a "save"
// is issued to create a new snapshot of the data in memory.

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
	public class PolyPersist
	{
		private static AutoResetEvent WaitHandle = new AutoResetEvent(false);

		private PolyConnection Connection;

		private static long MaxFileSize;

		private static long SizeAtSave;

		public static void Main(string[] args)
		{
			PolyPersist polyPersist = new PolyPersist();

			polyPersist.Run(args);
		}

		private void Run(string[] args)
		{
			string service = "8001";

			// Check the correct number of arguments have been supplied
			if (args.Length > 2)
			{
				Console.WriteLine("usage: {0} <max size of load_file> [<data service>]", System.AppDomain.CurrentDomain.FriendlyName);
				return;
			}

			// Maximum file size allowed
			MaxFileSize = long.Parse(args[0]);
			
			// Check whether a service argument has been supplied
			if (args.Length >= 2)
			{
				service = args[1];
			}

			// Build a connection string and connect to the database
			PolyConnectionStringBuilder builder = new PolyConnectionStringBuilder();

			builder.Service = service;

			Connection = new PolyConnection(builder.ConnectionString);

			// Register for state change events on the connection
			// This is used to detect loss of connection to the database
			Connection.StateChange += OnStateChange;

			Console.WriteLine("Connecting to database at {0}...", service);

			try
			{
				Connection.Open();
			}
			catch (Exception)
			{
				Console.WriteLine("Failed to connect to database");
				return;
			}

			// Create and command and an active adapter to perform the active query
			Console.WriteLine("Connected, now launch active query on journal control");
			Console.WriteLine("and monitor file_size for it reaching {0}", MaxFileSize);

			PolyCommand command = new PolyCommand("select id,file_size from journalcontrol", Connection);

			PolyActiveDataAdapter adapter = new PolyActiveDataAdapter(command);

			// Primary key information must be added to the data table
			adapter.MissingSchemaAction = MissingSchemaAction.AddWithKey;

			DataSet dataSet = new DataSet();

			// Perform an initial fill of the data table
			adapter.Fill(dataSet, "journalcontrol");

			DataTable dataTable = dataSet.Tables["journalcontrol"];

			// Display the results of the initial fill
			WriteTable(dataTable);

			// Register for data change events
			// This indicates when a delta is available for the active query
			adapter.DataChange += OnDataChange;

			while (WaitHandle.WaitOne())
			{
				// Stop when connection to the database is lost
				if (Connection.State == ConnectionState.Closed)
				{
					break;
				}

				// Apply the delta to the data table
				adapter.FillDelta(dataTable);

				// Display the results of the delta
				WriteTable(dataTable);
			}

			Connection.Close();
		}

		private void WriteTable(DataTable dataTable)
		{
			// Process the contents of the journalcontrol data table and issue a save when required
			foreach (DataRow dataRow in dataTable.Rows)
			{
				long file_size = (int)dataRow["file_size"];

				// SizeAtSave used to prevent false saves being issued as file_size fluctuates during save
				if (file_size < SizeAtSave)
				{
					// Ok to issue a save
					SizeAtSave = 0;
				}

				if (file_size > MaxFileSize && SizeAtSave == 0)
				{
					SaveDatabase(file_size);
				}
			}
		}

		private void SaveDatabase(long currentSize)
		{
			// The maximum allowable filesize has been exceeded so issue a save statement
			Console.WriteLine("File size has reached {0}, so time to create new load_file.", currentSize);

			SizeAtSave = currentSize;

			// Create a command and execute it in a transaction as a non-query to execute the save statement
			PolyTransaction transaction = Connection.BeginTransaction();

			// Enable safe-commit mode
			transaction.SafeCommit = true;

			PolyCommand command = new PolyCommand("save", Connection);

			command.Transaction = transaction;

			command.ExecuteNonQuery();

			try
			{
				transaction.Commit();
				Console.WriteLine("Save into completed.");
			}
			catch (Exception e)
			{
				Console.WriteLine("Failed to execute statement");
				WriteException(e);
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

		private static void OnDataChange(object sender, PolyDataChangeEventArgs args)
		{
			// A delta is available so wake-up the main thread
			WaitHandle.Set();
		}
	}
}

// End of file