using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Iot_Data.Models;  // Make sure to include the correct namespace for your models
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace Iot_Data.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly Iot_Data1Context _context;  // Add ApplicationDbContext

        public HomeController(ILogger<HomeController> logger, Iot_Data1Context context)
        {
            _logger = logger;
            _context = context;  // Initialize ApplicationDbContext
        }

        public IActionResult Index()
        {
            var nhietDos = _context.NhietDos.ToList();
            var doAms = _context.DoAms.ToList();
            var amThanhs = _context.AmThanhs.ToList();
            var gas = _context.Gas.ToList();
            var anhSangs = _context.AnhSangs.ToList();

            return View(new Tuple<List<NhietDo>, List<DoAm>, List<AmThanh>, List<Ga>, List<AnhSang>>(nhietDos, doAms, amThanhs, gas, anhSangs));
        }

        [HttpGet]
        public IActionResult GetData()
        {
            // Retrieve new sensor data from the database or any other source
            var newData = new
            {
                nhietDo = _context.NhietDos.ToList(),
                doAm = _context.DoAms.ToList(),
                amThanh = _context.AmThanhs.ToList(),
                ga = _context.Gas.ToList(),
                anhSang = _context.AnhSangs.ToList()
            };

            return Json(newData);
        }

        [HttpGet]
        public IActionResult GetLatestData()
        {
            var latestData = new
            {
                nhietDo = _context.NhietDos.OrderByDescending(x => x.ThoiGian).FirstOrDefault()?.GiaTri,
                doAm = _context.DoAms.OrderByDescending(x => x.ThoiGian).FirstOrDefault()?.GiaTri,
                amThanh = _context.AmThanhs.OrderByDescending(x => x.ThoiGian).FirstOrDefault()?.GiaTri,
                ga = _context.Gas.OrderByDescending(x => x.ThoiGian).FirstOrDefault()?.GiaTri,
                anhSang = _context.AnhSangs.OrderByDescending(x => x.ThoiGian).FirstOrDefault()?.GiaTri
            };

            return Json(latestData);
        }
        public IActionResult GetLatestDataType()
        {
            var latestDataType = new
            {
                nhannhietDo = _context.Predictions.OrderByDescending(x => x.Timestamp).FirstOrDefault()?.Label1,
                nhandoAm = _context.Predictions.OrderByDescending(x => x.Timestamp).FirstOrDefault()?.Label2,
                nhanamThanh = _context.Predictions.OrderByDescending(x => x.Timestamp).FirstOrDefault()?.Label3,
                nhanga = _context.Predictions.OrderByDescending(x => x.Timestamp).FirstOrDefault()?.Label4,
                nhananhSang = _context.Predictions.OrderByDescending(x => x.Timestamp).FirstOrDefault()?.Label5
            };

            return Json(latestDataType);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }

    }
}
