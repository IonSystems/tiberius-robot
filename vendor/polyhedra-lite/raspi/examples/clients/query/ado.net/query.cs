//
// Polyhedra ADO.NET Data Provider Query Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// This sample illustrates how a static query may be launched using the
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

namespace Polyhedra.Data.PolySample
{
	public class PolyQuery
	{
		public static void Main(string[] args)
		{
			PolyQuery polyQuery = new PolyQuery();

			polyQuery.Run(args);
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

			Console.WriteLine("Connecting to database at {0}...", service);

			try
			{
				connection.Open();
			}
			catch (Exception)
			{
				Console.WriteLine("Failed to connect to database");
				return;
			}

			// Create a command and execute a reader to perform the query
			Console.WriteLine("Connected, now launch query...");

			PolyCommand command = new PolyCommand("select * from currency", connection);

			PolyDataReader reader = command.ExecuteReader();

			while (reader.Read())
			{
				Console.WriteLine("Currency code: {0}: 1 US Dollar buys {1:F2} {2} {3}.", reader["code"], reader["usdollar"], reader["country"], reader["name"]);
			}

			Console.WriteLine("All rows returned.");

			reader.Close();

			connection.Close();
		}
	}
}

// End of file