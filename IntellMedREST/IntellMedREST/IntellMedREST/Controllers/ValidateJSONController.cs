using IntellMedREST.BusinessLogic;
using IntellMedREST.Data;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;


namespace IntellMedREST.Controllers
{

	[ApiController]
	[Route("[controller]")]
	public class ValidateJSONController : ControllerBase
	{

		private readonly ILogger<ValidateJSONController> _logger;

		public ValidateJSONController(ILogger<ValidateJSONController> logger)
		{
			_logger = logger;
		}


		[HttpPost("Test")]
		public async Task<IActionResult> Test()
		{
			var p = new Case();
			p.UploadDate = DateTime.Now;
			p.ID = 1;
			p.Fam = "Иванов";
			p.Im = "Иван";
			p.Ot = "Иванович";
			p.DB = DateTime.Now;
			p.DS = "J10.1";
			p.Stad = "средняя степень тяжести";
			p.Diags = new List<Diag>();

			var d1 = new Diag()
			{
				ID = 1,
				//Case=p,
				CodeUsl = "B01.014.001",
				UslName = "Прием (осмотр, консультация) врача-инфекциониста первичный",
				AvgQty = 1,
				AvgMultipl = 1
			};
			p.Diags.Add(d1);

			p.Lechs = new List<Lech>();

			var l1 = new Lech()
			{
				ID = 1,
				//Case = p,
				CodeUsl = "В01.028.001",
				UslName = "Прием (осмотр, консультация) врача-оториноларинголога первичный",
				AvgQty = 0.5M,
				AvgMultipl = 1
			};
			p.Lechs.Add(l1);


			p.Leks = new List<Lek>();

			var lr = new Lek()
			{
				ID = 1,
				//Case = p,
				Code = "A03FA",
				Class = "Стимуляторы моторики желудочно-кишечного тракта",
				Name = "Метоклопрамид",
				AvgQty = 0.3M,
				Uom = "мг",
				SSD = 15,
				SKD = 150
			};
			p.Leks.Add(lr);
			var k = new List<Case>();
			k.Add(p);
			string json = JsonConvert.SerializeObject(k, Formatting.Indented);
			return Ok();

		}



	

		[HttpPost("ValidateCase")]
		public async Task<IActionResult> ValidateCase(int id)
		{
			var db = new ApplicationContext();
			var  cs = 	db.Cases.Single<Case>(t=>t.ID==id);
			CaseVelidator.ValidateCase(cs);
			return Ok();
		}


		[HttpPost("UploadFiles")]
		public async Task<IActionResult> PostFile(List<IFormFile> files)
		{
			long size = files.Sum(f => f.Length);
			var filePath = Path.GetTempFileName();
			foreach (var formFile in files)
			{
				if (formFile.Length > 0)
				{
					using (var stream = new FileStream(filePath, FileMode.Create))
					{
						await formFile.CopyToAsync(stream);
					}
				}
			}
			var db = new ApplicationContext();
			var json = System.IO.File.ReadAllText(filePath);
			List<Case> persons = JsonConvert.DeserializeObject<List<Case>>(json);
			foreach (var p in persons)
			{
				db.Cases.Add(p);
			}
			db.SaveChanges();
			return Ok(new { count = files.Count, size, filePath });
		}
		 
	}
}
