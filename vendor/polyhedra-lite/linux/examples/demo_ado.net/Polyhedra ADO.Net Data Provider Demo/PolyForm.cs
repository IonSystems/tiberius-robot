//
// Polyhedra ADO.NET Data Provider DataGridView Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

// This sample illustrates how to use the Windows Forms DataGridView class with
// the Polyhedra ADO.NET data provider to display data changes from an active
// query and allow updates through the active query.

//-----------------------------------------------------------------------------
// NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
// demonstrate one or more features of the Polyhedra product.
// It may well need adaption for use in a live installation, and
// Enea Software AB and its agents and distributors do not warrant this code.
//-----------------------------------------------------------------------------

using Polyhedra.Data.PolyClient;
using System;
using System.ComponentModel;
using System.Data;
using System.Text;
using System.Windows.Forms;

namespace PolyDemo
{
	public partial class PolyForm : Form
	{
		PolyConnection connection;
		PolyActiveDataAdapter dataAdapter;
		PolyTransaction transaction;
		DataTable dataTable;
		String service = "8001";

		public PolyForm(string[] args)
		{
			// Check whether a service argument has been supplied
			if (args.Length != 0)
			{
				service = args[0];
			}

			InitializeComponent();

			// Include service in title
			Text = Text + String.Format(" - Service: {0}", service);

			Load += PolyForm_Load;
		}

		private void PolyForm_Load(object sender, EventArgs args)
		{
			// Build a connection string and connect to the database
			PolyConnectionStringBuilder builder = new PolyConnectionStringBuilder();

			builder.Service = service;

			connection = new PolyConnection(builder.ConnectionString);

			DialogResult result = DialogResult.Retry;

			// Allow connection attempt to be retried if it fails
			while (result == DialogResult.Retry)
			{
				try
				{
					connection.Open();
					break;
				}
				catch (Exception exception)
				{
					result = MessageBox.Show(GetExceptionMessage(exception), Text, MessageBoxButtons.RetryCancel);
					if (result != DialogResult.Retry)
					{
						Close();
						return;
					}
				}
			}

			// Create an active data adapter to perform the active query (on the currency table)
			dataAdapter = new PolyActiveDataAdapter("select * from currency", connection);

			// Create a data table to hold the data
			dataTable = new DataTable();

			// Primary key information must be added to the data table
			dataAdapter.MissingSchemaAction = MissingSchemaAction.AddWithKey;

			// Register for data change events
			// This indicates when a delta is available for the active query
			dataAdapter.DataChange += OnDataChange;

			// Do not automatically accept changes made to the data table when updating
			dataAdapter.AcceptChangesDuringUpdate = false;

			// Start active query and obtain initial data
			dataAdapter.Fill(dataTable);

			// Provide the data table as the data source to the data grid
			dataGridView.DataSource = dataTable;

			// Sort data by currency code
			dataGridView.Sort(dataGridView.Columns["code"], ListSortDirection.Ascending);

			// Right-align column containing dollar value
			dataGridView.Columns["usdollar"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleRight;

			// Turn edit mode off
			SetEditMode(false);

			// Note that the connection must remain open for the active data adapter to function
		}

		// Edit mode
		private void SetEditMode(bool editing)
		{
			// Only allow data grid content to be changed in edit mode
			dataGridView.ReadOnly = !editing;
			dataGridView.AllowUserToAddRows = editing;
			dataGridView.AllowUserToDeleteRows = editing;

			// Set appropriate title for Edit/Save button
			editSaveButton.Text = editing ? "Save" : "Edit";

			// Cancel button only visible in edit mode
			cancelButton.Enabled = editing;
			cancelButton.Visible = editing;
		}

		// Event handler called whenever a delta is received
		private void OnDataChange(object sender, PolyDataChangeEventArgs args)
		{
			// DataGridView changes must be run on the UI thread
			BeginInvoke((MethodInvoker)delegate
			{
				// Apply the delta to the data table and re-sort it
				dataAdapter.FillDelta(dataTable);
				dataTable.AcceptChanges();
				dataGridView.Sort(dataGridView.Columns["code"], ListSortDirection.Ascending);
				dataGridView.Refresh();
			});
		}

		// Edit/Save button
		private void editSaveButton_Click(object sender, System.EventArgs e)
		{
			if (transaction == null)
			{
				// Begin a transaction
				try
				{
					transaction = connection.BeginTransaction();
				}
				catch (Exception exception)
				{
					MessageBox.Show(GetExceptionMessage(exception) + " - exiting", Text, MessageBoxButtons.OK);
					Close();
					return;
				}

				dataAdapter.SelectCommand.Transaction = transaction;

				// Enable conflict detection on the transaction
				transaction.BeginConflictDetection();

				// Turn edit mode on
				SetEditMode(true);
			}
			else
			{
				// If changes have been made, commit them to the database
				if (dataTable.GetChanges() != null)
				{
					try
					{
						dataAdapter.Update(dataTable);
						transaction.Commit();
						dataTable.AcceptChanges();
					}
					catch (Exception exception)
					{
						MessageBox.Show(GetExceptionMessage(exception), Text);

						// Discard any changes made
						dataTable.RejectChanges();
					}
				}

				// Dispose of the transaction
				transaction.Dispose();
				transaction = null;

				// Turn edit mode off
				SetEditMode(false);
			}
		}

		// Cancel button
		private void cancelButton_Click(object sender, EventArgs e)
		{
			// Discard any changes made
			dataTable.RejectChanges();

			// Dispose of the transaction
			transaction.Dispose();
			transaction = null;

			// Turn edit mode off
			SetEditMode(false);
		}

		// Extract message from exception
		private String GetExceptionMessage(Exception exception)
		{
			if (exception is System.AggregateException)
			{
				StringBuilder builder = new StringBuilder();

				foreach (Exception innerException in ((System.AggregateException)exception).InnerExceptions)
				{
					if (builder.Length > 0)
						builder.Append(Environment.NewLine);

					builder.Append(innerException.Message);
				}

				return builder.ToString();
			}

			return exception.Message;
		}
	}
}

// End of file