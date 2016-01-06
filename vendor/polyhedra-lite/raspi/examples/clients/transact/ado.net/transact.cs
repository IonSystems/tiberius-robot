//
// Polyhedra ADO.NET Data Provider Transact Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// This sample illustrates how to execute a simple transaction using the
// Polyhedra ADO.NET data provider.
//
// It connects to the database and then fires off a piece of SQL,
// as specified by the program argument. 
//
// The supplied value can be a single SQL DDL statement
// (eg, create table, create schema, drop table), OR one or more SQL DML
// statements (insert, delete or update) separated by semicolons, but should
// not include any select statement.

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
	public class PolyTransact
	{
		public static void Main(string[] args)
		{
			PolyTransact polyTransact = new PolyTransact();

			polyTransact.Run(args);
		}

		private void Run(string[] args)
		{
			string service = "8001";

			// Check the correct number of arguments have been supplied
			if (args.Length < 1 || args.Length > 2)
			{
				Console.WriteLine("usage: {0} <sql> [<data service>]", System.AppDomain.CurrentDomain.FriendlyName);
				return;
			}

			string sql = args[0];

			// Check whether a service argument has been supplied
			if (args.Length >= 2)
			{
				service = args[1];
			}

			// Build a connection string and connect to the database
			PolyConnectionStringBuilder builder = new PolyConnectionStringBuilder();

			builder.Service = service;

			PolyConnection connection = new PolyConnection(builder.ConnectionString);

			Console.WriteLine("Connecting to port {0}...", service);

			try
			{
				connection.Open();
			}
			catch (Exception)
			{
				Console.WriteLine("Failed to connect to database");
				return;
			}

			Console.WriteLine("Connected successfully. Start the transaction:");
			Console.WriteLine("{0}", sql);

			// Create a command and execute it as a non-query to execute the statement
			PolyCommand command = new PolyCommand(sql, connection);

			try
			{
				command.ExecuteNonQuery();

				Console.WriteLine("Transaction completed successfully");
			}
			catch (Exception e)
			{
				Console.WriteLine("Failed to execute statement");

				WriteException(e);
			}
			finally
			{
				connection.Close();
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
	}
}

// End of file