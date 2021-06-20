using IntellMedREST.Classes;
using IntellMedREST.Data;
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

			var sqlStLek = "select * from \"Стандарты_Лекарства\" where \"КодСтандарта\"=" + Convert.ToInt32(singleCode[0]);
			var stLeks = Helper.RawSqlQuery<StLek>(sqlStLek, x => new StLek
			{
				Code = Convert.ToInt32(x[0]),
				StCode = Convert.ToInt32(x[1]),
				CodPrep = x[2].ToString(),
				Classif = x[3].ToString(),
				Name = x[4].ToString(),
				AvgQty = x[5] != null  ? (x[5]==string.Empty?null:Convert.ToDecimal(x[5].ToString())) : null,
				Uom = x[6].ToString(),
				SSD = x[7].ToString(),
				SKD = x[8].ToString()
			});


			var sqlStLech = "select * from \"Стандарты_Лечение\" where \"КодСтандарта\"=" + Convert.ToInt32(singleCode[0]);
			var  stLech = Helper.RawSqlQuery<StLech>(sqlStLech,
				x=> new StLech{
					Code = Convert.ToInt32(x[0]),
					StCode = Convert.ToInt32(x[1]),
					CodeUsl = x[2].ToString(),
					NameUsl = x[3].ToString(),
					AvgQty = Convert.ToDecimal(x[4]),
					AvgMult = Convert.ToDecimal(x[5])

				});


			var res = new System.Text.StringBuilder();

			// ищем все что ошибочно назначечно в диагностике де-факто
			foreach(var cseDiag in cse.Diags)
			{
				if (stDiags.Where(t=>t.CodeUsl==cseDiag.CodeUsl).Count()==0)
				{
					// не найден в стандарте
					res.Append(cseDiag.CodeUsl + " не найден в стандарте (ошибочно назначен) с кодом"+ singleCode);
				}
				
			}

			// ищем все что должно было быть назначено обязательно, но этого нет в диагностике
			foreach (var reqDiag in stDiags)
			{
				if (reqDiag.AvgQty==1)
				{
					// нету в лечении де-факто
					if (cse.Diags.Where(t=>t.CodeUsl==reqDiag.CodeUsl).Count()==0)
					{
						// не найден в лечении
						res.Append(reqDiag.CodeUsl + " не найден в лечении де-факто, но обязатален согласно стандарту с кодом" + singleCode);
					}
				}

			}





			return null;
		}


	}
}
