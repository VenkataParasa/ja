using Microsoft.AspNetCore.Mvc;
using JABizTown.API.Models;
using JABizTown.API.Services;

namespace JABizTown.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BusinessesController : ControllerBase
    {
        private readonly IBusinessService _businessService;
        private readonly ILogger<BusinessesController> _logger;

        public BusinessesController(IBusinessService businessService, ILogger<BusinessesController> logger)
        {
            _businessService = businessService;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Business>>> GetBusinesses()
        {
            try
            {
                var businesses = await _businessService.GetAllBusinessesAsync();
                return Ok(businesses);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving businesses");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Business>> GetBusiness(int id)
        {
            try
            {
                var business = await _businessService.GetBusinessByIdAsync(id);
                if (business == null)
                {
                    return NotFound();
                }
                return Ok(business);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving business with ID: {BusinessId}", id);
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPost]
        public async Task<ActionResult<Business>> CreateBusiness(Business business)
        {
            try
            {
                var createdBusiness = await _businessService.CreateBusinessAsync(business);
                return CreatedAtAction(nameof(GetBusiness), new { id = createdBusiness.BusinessId }, createdBusiness);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating business");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateBusiness(int id, Business business)
        {
            try
            {
                if (id != business.BusinessId)
                {
                    return BadRequest();
                }

                var updatedBusiness = await _businessService.UpdateBusinessAsync(id, business);
                return Ok(updatedBusiness);
            }
            catch (KeyNotFoundException)
            {
                return NotFound();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating business with ID: {BusinessId}", id);
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBusiness(int id)
        {
            try
            {
                var result = await _businessService.DeleteBusinessAsync(id);
                if (!result)
                {
                    return NotFound();
                }
                return NoContent();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting business with ID: {BusinessId}", id);
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPut("{id}/balance")]
        public async Task<ActionResult<Business>> UpdateBalance(int id, [FromBody] decimal newBalance)
        {
            try
            {
                var business = await _businessService.UpdateBusinessBalanceAsync(id, newBalance);
                if (business == null)
                {
                    return NotFound();
                }
                return Ok(business);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating balance for business ID: {BusinessId}", id);
                return StatusCode(500, "Internal server error");
            }
        }
    }
}
