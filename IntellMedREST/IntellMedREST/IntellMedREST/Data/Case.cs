using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IntellMedREST.Data
{
	public class Case
	{
		public int ID { get;set; }
		public DateTime UploadDate { get; set; }
		public string Fam { get; set; }
		public string Im { get; set; }
		public string Ot { get; set; }
		public DateTime DB { get; set; }
		public string DS { get; set; }
		public string Stad { get; set; }
		public ICollection<Diag> Diags { get; set; }
		public ICollection<Lech> Lechs { get; set; }
		public ICollection<Lek> Leks { get; set; }
	}
}
