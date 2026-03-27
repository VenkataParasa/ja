using System.ComponentModel.DataAnnotations;

namespace JABizTown.API.Models
{
    public class SimulationState
    {
        [Key]
        public int Id { get; set; }
        
        [Required]
        [MaxLength(20)]
        public string Status { get; set; } = "Active"; // Active, Paused, Completed
        
        public bool IsTornadoActive { get; set; } = false; // Legacy/Fallback
        
        [MaxLength(50)]
        public string ActiveIncident { get; set; } = "None"; // e.g., "None", "Tornado", "Power Outage", "News Flash"
        
        [MaxLength(500)]
        public string IncidentMessage { get; set; } = string.Empty;
        
        public string XPData { get; set; } = "{}"; // JSON map of BusinessId to XP points
        
        public string ContributionData { get; set; } = "{}"; // JSON map of BusinessId to decision
        
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    }
}
