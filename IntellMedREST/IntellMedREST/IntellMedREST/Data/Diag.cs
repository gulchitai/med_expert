using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IntellMedREST.Data
{
	public class Diag
	{
		public int ID { get; set; }
		public Case Case { get; set; }
		public string CodeUsl { get; set; }
		public string UslName { get; set; }
		public decimal AvgQty { get; set; }
		public decimal AvgMultipl { get; set; }
	}
}
