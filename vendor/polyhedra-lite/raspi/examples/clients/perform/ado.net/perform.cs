//
// Polyhedra ADO.NET Data Provider Perform Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// Performance test application

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
using System.Data.Odbc;
using System.Diagnostics;
using System.Text;

namespace Polyhedra.Data.PolySample
{
	public class PolyPerform
	{
		private DbConnection Connection;
		private string Service = "8001";
		private int RowCount = 10000;
		private int BatchSize = 100;

		public static void Main(string[] args)
		{
			PolyPerform polyPerform = new PolyPerform();

			polyPerform.Run(args);
		}

		private void Run(string[] args)
		{
			// Check the correct number of arguments have been supplied
			if (args.Length > 3)
			{
				Console.WriteLine("usage: {0} [<service>] [<row count>] [<batch size>]", System.AppDomain.CurrentDomain.FriendlyName);
				return;
			}

			// Check whether a service argument has been supplied
			if (args.Length >= 1)
			{
				Service = args[0];
			}

			// Check whether a row count argument has been supplied
			if (args.Length >= 2)
			{
				RowCount = int.Parse(args[1]);
			}

			// Check whether a buffer size argument has been supplied
			if (args.Length >= 3)
			{
				BatchSize = int.Parse(args[2]);
			}

			// Build a connection string and connect to the database
			Connection = new PolyConnection();
			PolyConnectionStringBuilder builder = new PolyConnectionStringBuilder();

			builder.Service = Service;

			Connection.ConnectionString = builder.ConnectionString;

			try
			{
				Connection.Open();
			}
			catch (Exception)
			{
				Console.WriteLine("Failed to connect to database");
				return;
			}

			Console.WriteLine("Database:       {0}", Connection.Database);
			Console.WriteLine("Data Source:    {0}", Connection.DataSource);
			Console.WriteLine("Server Version: {0}", Connection.ServerVersion);
			Console.WriteLine("");

			// Run performance tests

			QueryRows(5, 1, RowCount);
			QueryRows(50, 1, RowCount);
			QueryRows(5, BatchSize, RowCount);
			QueryRows(5, 1, 10 * RowCount);

			InsertRows(5, 1, 0);
			InsertRows(50, 1, 0);
			InsertRows(5, BatchSize, 0);
			InsertRows(5, 1, 10 * RowCount);

			UpdateRows(5, 1, RowCount);
			UpdateRows(50, 1, RowCount);
			UpdateRows(5, BatchSize, RowCount);
			UpdateRows(5, 1, 10 * RowCount);

			DeleteRows(5, 1, RowCount);
			DeleteRows(50, 1, RowCount);
			DeleteRows(5, BatchSize, RowCount);
			DeleteRows(5, 1, 10 * RowCount);

			Connection.Close();
		}

		// Derived standard test name
		private String TestName(String prefix, int columnCount, int batchSize, bool populate)
		{
			return String.Format("{0}{1}{2}{3}", prefix, columnCount, batchSize > 1 ? "B" : "", populate ? "P" : "");
		}

		// Create test table with specified number of columns
		private void CreateTable(int columnCount)
		{
			DbCommand command = Connection.CreateCommand();

			StringBuilder sqlBuilder = new StringBuilder();

			sqlBuilder.Append("create table test (id integer primary key");

			for (int col = 2; col <= columnCount; col++)
			{
				sqlBuilder.AppendFormat(",col{0} integer", col);
			}

			sqlBuilder.Append(")");

			command.CommandText = sqlBuilder.ToString();

			command.ExecuteNonQuery();
		}

		// Drop test table
		private void DropTable()
		{
			DbCommand command = Connection.CreateCommand();

			command.CommandText = "drop table test";

			command.ExecuteNonQuery();
		}

		// Populate the test table with the specified number of columns and rows
		private void PopulateTable(int columnCount, int populateCount)
		{
			DbCommand command = Connection.CreateCommand();

			StringBuilder sqlBuilder = new StringBuilder();

			sqlBuilder.Append("insert into test (id");

			for (int col = 2; col <= columnCount; col++)
			{
				sqlBuilder.AppendFormat(",col{0}", col);
			}

			sqlBuilder.Append(") values (?");

			for (int col = 2; col <= columnCount; col++)
			{
				sqlBuilder.Append(",?");
			}

			sqlBuilder.Append(")");

			command.CommandText = sqlBuilder.ToString();

			command.Prepare();

			DbParameter parameter = command.CreateParameter();

			command.Parameters.Add(parameter);

			for (int col = 2; col <= columnCount; col++)
			{
				parameter = command.CreateParameter();

				command.Parameters.Add(parameter);
			}

			DbTransaction transaction = null;

			for (int i = 0; i < populateCount; i++)
			{
				if (i % 1000 == 0)
				{
					if (i != 0) transaction.Commit();

					transaction = Connection.BeginTransaction();
				}

				command.Transaction = transaction;

				for (int col = 1; col <= columnCount; col++)
				{
					command.Parameters[col - 1].Value = i;
				}

				command.ExecuteNonQuery();
			}

			transaction.Commit();
		}

		// Query performance test
		private void QueryRows(int columnCount, int batchSize, int populateCount)
		{
			CreateTable(columnCount);

			PopulateTable(columnCount, populateCount);

			DbCommand command = Connection.CreateCommand();

			if (batchSize > 1)
			{
				StringBuilder sqlBuilder = new StringBuilder();

				sqlBuilder.Append("select * from test where id in (");

				for (int id = 0; id < batchSize; id++)
				{
					if (id != 0) sqlBuilder.Append(",");
					sqlBuilder.Append("?");
				}

				sqlBuilder.Append(")");

				command.CommandText = sqlBuilder.ToString();
			}
			else
			{
				command.CommandText = "select * from test where id=?";
			}

			command.Prepare();

			for (int id = 0; id < batchSize; id++)
			{
				DbParameter parameter = command.CreateParameter();

				command.Parameters.Add(parameter);
			}

			Stopwatch stopwatch = new Stopwatch();

			stopwatch.Start();

			for (int i = 0; i < RowCount; i += batchSize)
			{
				for (int id = 0; id < batchSize; id++)
				{
					command.Parameters[id].Value = i + id;
				}

				DbDataReader reader = command.ExecuteReader();

				if (batchSize > 1)
				{
					for (int j = 0; (j < batchSize) && (i + j < RowCount); j++)
					{
						reader.Read();
					}
				}
				else
				{
					reader.Read();
				}
				reader.Close();
			}

			stopwatch.Stop();

			Console.WriteLine("\tquery {0} records ({1} per query) ({2})", RowCount, batchSize, TestName("Q", columnCount, batchSize, populateCount != RowCount));
			Console.WriteLine("\t(records in table at start: {0})", populateCount);
			Console.WriteLine("\ttime: {0:F2}", stopwatch.ElapsedMilliseconds / 1000.0);
			Console.WriteLine("\ttps: {0:F0}", RowCount / (stopwatch.ElapsedMilliseconds / 1000.0));
			Console.WriteLine("");

			DropTable();
		}

		// Insert performance test
		private void InsertRows(int columnCount, int batchSize, int populateCount)
		{
			CreateTable(columnCount);

			if (populateCount > 0)
			{
				PopulateTable(columnCount, populateCount);
			}

			DbCommand command = Connection.CreateCommand();

			StringBuilder sqlBuilder = new StringBuilder();

			sqlBuilder.Append("insert into test (id");

			for (int col = 2; col <= columnCount; col++)
			{
				sqlBuilder.AppendFormat(",col{0}", col);
			}

			sqlBuilder.Append(") values (?");

			for (int col = 2; col <= columnCount; col++)
			{
				sqlBuilder.Append(",?");
			}

			sqlBuilder.Append(")");

			command.CommandText = sqlBuilder.ToString();

			command.Prepare();

			DbParameter parameter = command.CreateParameter();

			command.Parameters.Add(parameter);

			for (int col = 2; col <= columnCount; col++)
			{
				parameter = command.CreateParameter();

				command.Parameters.Add(parameter);
			}

			DbTransaction transaction = null;

			Stopwatch stopwatch = new Stopwatch();

			stopwatch.Start();

			for (int i = 0; i < RowCount; i++)
			{
				if (batchSize > 1)
				{
					if (i % batchSize == 0)
					{
						if (i != 0) transaction.Commit();

						transaction = Connection.BeginTransaction();
					}

					command.Transaction = transaction;
				}

				for (int col = 1; col <= columnCount; col++)
				{
					command.Parameters[col - 1].Value = i + populateCount;
				}

				command.ExecuteNonQuery();
			}

			if (batchSize > 1)
			{
				transaction.Commit();
			}

			stopwatch.Stop();

			Console.WriteLine("\tinsert {0} records ({1} per transaction) ({2})", RowCount, batchSize, TestName("I", columnCount, batchSize, populateCount != 0));
			Console.WriteLine("\t(records in table at start: {0})", populateCount);
			Console.WriteLine("\ttime: {0:F2}", stopwatch.ElapsedMilliseconds / 1000.0);
			Console.WriteLine("\ttps: {0:F0}", RowCount / (stopwatch.ElapsedMilliseconds / 1000.0));
			Console.WriteLine("");

			DropTable();
		}

		// Update performance test
		private void UpdateRows(int columnCount, int batchSize, int populateCount)
		{
			CreateTable(columnCount);

			PopulateTable(columnCount, populateCount);

			DbCommand command = Connection.CreateCommand();

			StringBuilder sqlBuilder = new StringBuilder();

			sqlBuilder.Append("update test set ");

			for (int col = 2; col <= columnCount; col++)
			{
				if (col != 2) sqlBuilder.Append(",");
				sqlBuilder.AppendFormat("col{0}=?", col);
			}

			sqlBuilder.Append(" where id=?");

			command.CommandText = sqlBuilder.ToString();

			command.Prepare();

			DbParameter parameter = command.CreateParameter();

			command.Parameters.Add(parameter);

			for (int col = 2; col <= columnCount; col++)
			{
				parameter = command.CreateParameter();

				command.Parameters.Add(parameter);
			}

			DbTransaction transaction = null;

			Stopwatch stopwatch = new Stopwatch();

			stopwatch.Start();

			for (int i = 0; i < RowCount; i++)
			{
				if (batchSize > 1)
				{
					if (i % batchSize == 0)
					{
						if (i != 0) transaction.Commit();

						transaction = Connection.BeginTransaction();
					}

					command.Transaction = transaction;
				}

				for (int col = 1; col <= columnCount; col++)
				{
					command.Parameters[col - 1].Value = i;
				}

				command.ExecuteNonQuery();
			}

			if (batchSize > 1)
			{
				transaction.Commit();

				command.Transaction = null;
			}

			stopwatch.Stop();

			Console.WriteLine("\tupdate {0} records ({1} per transaction) ({2})", RowCount, batchSize, TestName("U", columnCount, batchSize, populateCount != RowCount));
			Console.WriteLine("\t(records in table at start: {0})", populateCount);
			Console.WriteLine("\ttime: {0:F2}", stopwatch.ElapsedMilliseconds / 1000.0);
			Console.WriteLine("\ttps: {0:F0}", RowCount / (stopwatch.ElapsedMilliseconds / 1000.0));
			Console.WriteLine("");

			DropTable();
		}

		// Delete performance test
		private void DeleteRows(int columnCount, int batchSize, int populateCount)
		{
			CreateTable(columnCount);

			PopulateTable(columnCount, populateCount);

			DbCommand command = Connection.CreateCommand();

			command.CommandText = "delete from test where id=?";

			command.Prepare();

			DbParameter parameter = command.CreateParameter();

			command.Parameters.Add(parameter);

			DbTransaction transaction = null;

			Stopwatch stopwatch = new Stopwatch();

			stopwatch.Start();

			for (int i = 0; i < RowCount; i++)
			{
				if (batchSize > 1)
				{
					if (i % batchSize == 0)
					{
						if (i != 0) transaction.Commit();

						transaction = Connection.BeginTransaction();
					}

					command.Transaction = transaction;
				}

				parameter.Value = i;

				command.ExecuteNonQuery();
			}

			if (batchSize > 1)
			{
				transaction.Commit();

				command.Transaction = null;
			}

			stopwatch.Stop();

			Console.WriteLine("\tdelete {0} records ({1} per transaction) ({2})", RowCount, batchSize, TestName("D", columnCount, batchSize, populateCount != RowCount));
			Console.WriteLine("\t(records in table at start: {0})", populateCount);
			Console.WriteLine("\ttime: {0:F2}", stopwatch.ElapsedMilliseconds / 1000.0);
			Console.WriteLine("\ttps: {0:F0}", RowCount / (stopwatch.ElapsedMilliseconds / 1000.0));
			Console.WriteLine("");

			DropTable();
		}
	}
}

// End of file