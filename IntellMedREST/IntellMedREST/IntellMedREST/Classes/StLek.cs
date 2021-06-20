using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IntellMedREST.Classes
{
	public class StLek
	{
		public int Code { get; set; }
		public int StCode { get; set; }
		public string CodPrep { get; set; }
		public string Classif { get; set; }
		public string Name { get; set; }
		public decimal AvgQty { get; set; }
		public string Uom { get; set; }
		public string SSD { get; set; }
		public string SKD { get; set; }
	}
}
