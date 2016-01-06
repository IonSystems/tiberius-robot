//
// Polyhedra ADO.NET Data Provider Monitor Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// This sample illustrates how active queries can be used to monitor changes in
// a table using the Polyhedra ADO.NET data provider.
// A message is produced when a new currency_limit is set up, and when the
// current value moves into or outside the limits associated with the currency.

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
	public class PolyMonitor
	{
		private static AutoResetEvent WaitHandle = new AutoResetEvent(false);

		private enum Alarm
		{
			UNKNOWN_ALARM,
			NO_ALARM,
			LO_ALARM,
			HI_ALARM
		};

		public static void Main(string[] args)
		{
			PolyMonitor polyMonitor = new PolyMonitor();

			polyMonitor.Run(args);
		}

		private void Run(string[] args)
		{
			string service = "8001";

			// Check the correct number of arguments have been supplied
			if (args.Length > 1)
			{
				Console.WriteLine("usage: {0} [<data service>]", System.AppDomain.CurrentDomain.FriendlyName);
				return;
			}

			// Check whether a service argument has been supplied
			if (args.Length >= 1)
			{
				service = args[0];
			}

			// Build a connection string and connect to the database
			PolyConnectionStringBuilder builder = new PolyConnectionStringBuilder();

			builder.Service = service;

			PolyConnection connection = new PolyConnection(builder.ConnectionString);

			// Register for state change events on the connection
			// This is used to detect loss of connection to the database
			connection.StateChange += OnStateChange;

			Console.WriteLine("Connecting to {0}...", service);

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

			PolyCommand command = new PolyCommand("select code,usdollar,low_limit,high_limit from currency_limits", connection);

			PolyActiveDataAdapter adapter = new PolyActiveDataAdapter(command);

			// Primary key information must be added to the data table
			adapter.MissingSchemaAction = MissingSchemaAction.AddWithKey;

			DataSet dataSet = new DataSet();

			// Explicitly accept changes made to the data table by the delta
			adapter.AcceptChangesDuringFill = false;

			// Register for data change events
			// This indicates when a delta is available for the active query
			adapter.DataChange += OnDataChange;

			// Perform an initial fill of the data table
			adapter.Fill(dataSet, "currency_limits");

			DataTable dataTable = dataSet.Tables["currency_limits"];

			// Display the results of the initial fill
			WriteTable(dataTable);

			// Accept the changes made to the data table by the delta
			dataTable.AcceptChanges();

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

				// Display the results of the delta
				WriteTable(dataTable);

				// Accept the changes made to the data table by the delta
				dataTable.AcceptChanges();
			}

			connection.Close();
		}

		private void WriteTable(DataTable dataTable)
		{
			// Process the contents of the currency_limits data table and display alarms
			foreach (DataRow dataRow in dataTable.Rows)
			{
				string code = (string)dataRow["code"];
				double high_limit = (double)dataRow["high_limit"];
				double low_limit = (double)dataRow["low_limit"];
				double usdollar = (double)dataRow["usdollar"];

				Alarm newAlarm = ((usdollar > high_limit) ? Alarm.HI_ALARM : ((usdollar < low_limit) ? Alarm.LO_ALARM : Alarm.NO_ALARM));

				Alarm oldAlarm = Alarm.UNKNOWN_ALARM;

				// Determine the old alarm from the orginal values in the data row, if present
				if (dataRow.RowState != DataRowState.Added)
				{
					double old_high_limit = (double)dataRow["high_limit", DataRowVersion.Original];
					double old_low_limit = (double)dataRow["low_limit", DataRowVersion.Original];
					double old_usdollar = (double)dataRow["usdollar", DataRowVersion.Original];

					oldAlarm = ((old_usdollar > old_high_limit) ? Alarm.HI_ALARM : ((old_usdollar < old_low_limit) ? Alarm.LO_ALARM : Alarm.NO_ALARM));
				}

				if (newAlarm != oldAlarm)
				{
					if (oldAlarm == Alarm.UNKNOWN_ALARM)
					{
						Console.WriteLine("Row Added - Code: {0}, 1 Dollar buys: {1:F2}. Limits - Low: {2:F2} High: {3:F2}", code, usdollar, low_limit, high_limit);
					}
					else if (newAlarm == Alarm.HI_ALARM)
					{
						Console.WriteLine("*** ALARM *** : {0} has risen above the high alarm limit {1:F2} at {2:F2}.", code, high_limit, usdollar);
					}
					else if (newAlarm == Alarm.LO_ALARM)
					{
						Console.WriteLine("*** ALARM *** : {0} has dropped below the low alarm limit {1:F2} at {2:F2}.", code, low_limit, usdollar);
					}
					else if (oldAlarm == Alarm.LO_ALARM)
					{
						Console.WriteLine("--- clear --- : {0} has risen above the low alarm limit {1:F2} at {2:F2}.", code, low_limit, usdollar);
					}
					else if (oldAlarm == Alarm.HI_ALARM)
					{
						Console.WriteLine("--- clear --- : {0} has dropped below the high alarm limit {1:F2} at {2:F2}.\n", code, high_limit, usdollar);
					}
					else
					{
						Console.WriteLine("{0} lies within limits ({1:F2}, {2:F2}) at {3:F3}.\n", code, low_limit, high_limit, usdollar);
					}
				}
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