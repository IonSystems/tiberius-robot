//
// Polyhedra ADO.NET Data Provider Active Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// This sample illustrates how an active query may be launched using the
// Polyhedra ADO.NET data provider.

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
	public class PolyActive
	{
		private static AutoResetEvent WaitHandle = new AutoResetEvent(false);

		public static void Main(string[] args)
		{
			PolyActive polyActive = new PolyActive();

			polyActive.Run(args);
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

			// Create and command and an active adapter to perform the active query
			Console.WriteLine("Connected, now launch active query...");

			PolyCommand command = new PolyCommand("select code,usdollar from currency", connection);

			PolyActiveDataAdapter adapter = new PolyActiveDataAdapter(command);

			// Primary key information must be added to the data table
			adapter.MissingSchemaAction = MissingSchemaAction.AddWithKey;

			DataSet dataSet = new DataSet();

			// Perform an initial fill of the data table
			adapter.Fill(dataSet, "currency");

			DataTable dataTable = dataSet.Tables["currency"];

			// Display the results of the initial fill
			WriteTable(dataTable);

			// Register for data change events
			// This indicates when a delta is available for the active query
			adapter.DataChange += OnDataChange;

			// Register for row changed and row deleted events on the data table
			// This is used to determine the changes made when applying a delta
			dataTable.RowChanged += OnRowChanged;
			dataTable.RowDeleted += OnRowDeleted;

			// Explicitly accept changes made to the data table by the delta
			adapter.AcceptChangesDuringFill = false;

			// Use the Upsert LoadOption to determine the changes made by the delta
			adapter.FillLoadOption = LoadOption.Upsert;

			while (WaitHandle.WaitOne())
			{
				// Stop when connection to the database is lost
				if (connection.State == ConnectionState.Closed)
				{
					break;
				}

				// Apply the delta to the data table
				adapter.FillDelta(dataTable);

				Console.WriteLine("Delta complete - success.\n");

				// Accept the changes made to the data table by the delta
				dataTable.AcceptChanges();
			}

			connection.Close();
		}

		private void WriteTable(DataTable dataTable)
		{
			// Display the contents of the currency data table
			foreach (DataRow dataRow in dataTable.Rows)
			{
				Console.WriteLine("Row Added - Code: {0}, 1 Dollar buys: {1:F6}.", dataRow["code"], dataRow["usdollar"]);
			}

			Console.WriteLine("Delta complete - success.\n");
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

		private static void OnRowChanged(object sender, DataRowChangeEventArgs args)
		{
			// A row has either been added or changed by the delta
			DataRow dataRow = args.Row;

			switch (args.Action)
			{
				case DataRowAction.Add:
					Console.WriteLine("Row Added - Code: {0} 1 Dollar buys: {1:F6}.", dataRow["code"], dataRow["usdollar"]);
					break;

				case DataRowAction.Change:
					Console.WriteLine("Code: {0}, 1 US Dollar now buys: {1:F6}.", dataRow["code"], dataRow["usdollar"]);
					break;
			}
		}

		private static void OnRowDeleted(object sender, DataRowChangeEventArgs args)
		{
			// A row has been deleted by the delta
			Console.WriteLine("Currency {0} removed from resultset", args.Row["code"]);
		}
	}
}

// End of file