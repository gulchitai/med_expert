﻿using IntellMedREST.Data;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Data.SqlClient;
using System.Linq;
using System.Threading.Tasks;

namespace IntellMedREST.BusinessLogic
{



	public class StDiag
	{
		public int Code { get; set; }
		public int StCode { get; set; }
		public string CodeUsl { get; set; }
		public string NameUsl { get; set; }
		public decimal AvgQty { get; set; }
		public decimal AvgMult { get; set; }
	}

	public class CaseVelidator
	{
		

		public static string ValidateCase(Case cse)
		{
            var db = new ApplicationContext();
			var ds = cse.DS;
            var codes = Helper.RawSqlQuery<Int64>("select \"КодСтандарта\" from \"Стандарты_МКБ\" where \"КодМКБ\" like '%J10.1%'",x=>(Int64)x[0]);
            var strCodeCond = "(";
            foreach (var code in codes)
			{
                strCodeCond+=code+",";
			}
            strCodeCond+=")";
            strCodeCond = strCodeCond.Replace(",)",")"); // :)
            var daysAge = DateTime.Now.Subtract(cse.DB).Days;
            var yearsAge = daysAge / 365; 
            var isDet="0";
            if (yearsAge>18)
			{
                isDet="0";
			}
			else
			{
                isDet="1";
			}
            var sqlSingleCode = "select \"Код\"  from \"Стандарты\" where \"Код\" in " + strCodeCond + " and \"Дети\"="+isDet;
            var singleCode = Helper.RawSqlQuery<Int64>(sqlSingleCode, x => (Int64)x[0]);

			var   sqlStDiags = "select * from \"Стандарты_Диагностика\" where \"КодСтандарта\"="+Convert.ToInt32(singleCode[0]);
			var stDiags = Helper.RawSqlQuery<StDiag>(sqlStDiags, x => new StDiag{ Code=Convert.ToInt32(x[0]), StCode= Convert.ToInt32(x[1]), CodeUsl = x[2].ToString(), NameUsl = x[3].ToString(), AvgQty = Convert.ToDecimal(x[4]), AvgMult = Convert.ToDecimal(x[5]) });





			return null;
		}


	}
}