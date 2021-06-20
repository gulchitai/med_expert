using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IntellMedREST.Data
{

	public class Lek
	{
		public int ID { get; set; }
		public Case Case { get; set; }
		public string Code { get; set; }
		public string Class { get; set; }
		public string Name { get; set; }
		public decimal AvgQty { get; set; }
		public string Uom { get; set; }
		public decimal SSD { get; set; }
		public decimal SKD { get; set; }
	}
}
