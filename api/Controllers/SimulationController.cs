using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using JABizTown.API.Data;
using JABizTown.API.Models;

namespace JABizTown.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SimulationController : ControllerBase
    {
        private readonly JABizTownDbContext _context;
        private readonly ILogger<SimulationController> _logger;

        public SimulationController(JABizTownDbContext context, ILogger<SimulationController> logger)
        {
            _context = context;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<SimulationState>> GetState()
        {
            var state = await _context.SimulationStates.FirstOrDefaultAsync();
            if (state == null)
            {
                state = new SimulationState { Status = "Active", IsTornadoActive = false };
                _context.SimulationStates.Add(state);
                await _context.SaveChangesAsync();
            }
            return Ok(state);
        }

        [HttpPost("toggle-tornado")]
        public async Task<ActionResult<SimulationState>> ToggleTornado([FromBody] bool active)
        {
            var state = await _context.SimulationStates.FirstOrDefaultAsync();
            if (state == null)
            {
                state = new SimulationState();
                _context.SimulationStates.Add(state);
            }
            
            // Clear previous contributions if we are triggering a new incident
            if (active && !state.IsTornadoActive)
            {
                state.ContributionData = "{}";
                _logger.LogInformation("New Tornado incident triggered - cleared previous contributions");
            }
            
            state.IsTornadoActive = active;
            state.ActiveIncident = active ? "Tornado" : "None";
            state.IncidentMessage = active ? "A Tornado has struck the park! Decide how to respond." : "";
            state.UpdatedAt = DateTime.UtcNow;
            
            await _context.SaveChangesAsync();
            return Ok(state);
        }

        [HttpPost("trigger-incident")]
        public async Task<ActionResult<SimulationState>> TriggerIncident([FromBody] IncidentRequest request)
        {
            var state = await _context.SimulationStates.FirstOrDefaultAsync();
            if (state == null)
            {
                state = new SimulationState();
                _context.SimulationStates.Add(state);
            }

            // Clear previous contributions if triggering a new incident
            if (request.IncidentType != "None" && state.ActiveIncident != request.IncidentType)
            {
                state.ContributionData = "{}";
                _logger.LogInformation($"New {request.IncidentType} incident triggered - cleared previous contributions");
            }

            state.ActiveIncident = request.IncidentType;
            state.IncidentMessage = request.IncidentMessage;
            state.IsTornadoActive = request.IncidentType == "Tornado";
            state.UpdatedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();
            return Ok(state);
        }

        [HttpPost("status")]
        public async Task<ActionResult<SimulationState>> UpdateStatus([FromBody] string status)
        {
            var state = await _context.SimulationStates.FirstOrDefaultAsync();
            if (state == null)
            {
                state = new SimulationState();
                _context.SimulationStates.Add(state);
            }
            
            state.Status = status;
            state.UpdatedAt = DateTime.UtcNow;
            
            await _context.SaveChangesAsync();
            return Ok(state);
        }

        [HttpPost("update-data")]
        public async Task<ActionResult<SimulationState>> UpdateData([FromBody] SimulationStateUpdateDto dto)
        {
            var state = await _context.SimulationStates.FirstOrDefaultAsync();
            if (state == null)
            {
                state = new SimulationState();
                _context.SimulationStates.Add(state);
            }
            
            if (dto.XPData != null) state.XPData = dto.XPData;
            if (dto.ContributionData != null) state.ContributionData = dto.ContributionData;
            state.UpdatedAt = DateTime.UtcNow;
            
            await _context.SaveChangesAsync();
            return Ok(state);
        }
    }

    public class SimulationStateUpdateDto
    {
        public string? XPData { get; set; }
        public string? ContributionData { get; set; }
    }

    public class IncidentRequest
    {
        public string IncidentType { get; set; } = "None";
        public string IncidentMessage { get; set; } = string.Empty;
    }
}
