//
// Polyhedra ADO.NET Data Provider DataGridView Sample
//
// Copyright (C) 1994-2015 by Enea Software AB
// All Rights Reserved
//

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PolyDemo
{
	static class Program
	{
		/// <summary>
		/// The main entry point for the application.
		/// </summary>
		[STAThread]
		static void Main(string[] args)
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new PolyForm(args));
		}
	}
}

// End of file