using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IntellMedREST.Classes
{
	public class StLech
	{
		public int Code { get; set; }
		public int StCode { get; set; }
		public string CodeUsl { get; set; }
		public string NameUsl { get; set; }
		public decimal AvgQty { get; set; }
		public decimal AvgMult { get; set; }
	}
}
