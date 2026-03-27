using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using JABizTown.API.Data;
using JABizTown.API.Models;

namespace JABizTown.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class LeaderboardController : ControllerBase
    {
        private readonly JABizTownDbContext _context;

        public LeaderboardController(JABizTownDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<LeaderboardEntry>>> GetLeaderboard()
        {
            var businesses = await _context.Businesses.ToListAsync();
            var leaderboard = businesses.Select(b => CalculateScore(b))
                .OrderByDescending(e => e.TotalScore)
                .ToList();

            // Assign ranks
            for (int i = 0; i < leaderboard.Count; i++)
            {
                leaderboard[i].Rank = i + 1;
            }

            return Ok(leaderboard);
        }

        private LeaderboardEntry CalculateScore(Business b)
        {
            // 1. Financial Health (Max 400)
            decimal loanProgress = b.LoanAmount > 0 ? (b.LoanPaid / b.LoanAmount) : 1;
            double loanScore = (double)loanProgress * 200;

            decimal profitMargin = b.InitialCapital > 0 ? (b.CurrentBalance - b.InitialCapital) / b.InitialCapital : 0;
            double profitScore = Math.Min(200, Math.Max(0, (double)profitMargin * 1000)); // 20% profit = 200 pts

            double financialScore = loanScore + profitScore;

            // 2. Efficiency (Max 300)
            double efficiencyScore = b.EfficiencyScore * 3; // Base 0-100 map to 0-300

            // 3. Civic Virtue (Max 300)
            double civicScore = Math.Min(300, (double)(b.PhilanthropicTotal / 500m) * 300);

            double totalScore = financialScore + efficiencyScore + civicScore;

            var entry = new LeaderboardEntry
            {
                BusinessId = b.BusinessId,
                BusinessName = b.BusinessName,
                BusinessType = b.BusinessType,
                TotalScore = (int)Math.Round(totalScore),
                FinancialScore = (int)Math.Round(financialScore),
                EfficiencyScore = (int)Math.Round(efficiencyScore),
                CivicScore = (int)Math.Round(civicScore),
                Tips = GenerateTips(b, loanProgress, profitMargin)
            };

            return entry;
        }

        private List<string> GenerateTips(Business b, decimal loanProgress, decimal profitMargin)
        {
            var tips = new List<string>();

            if (loanProgress < 0.5m)
                tips.Add("Focus on paying down your business loan to reduce interest and boost your score.");
            
            if (profitMargin < 0.1m)
                tips.Add("Review your product pricing. Ensure your profit margin is above 10% to stay competitive.");

            if (b.PhilanthropicTotal < 100)
                tips.Add("Consider increasing your philanthropic contributions to improve your 'Civic Virtue' rating.");

            if (b.EfficiencyScore < 80)
                tips.Add("Your payment processing speed is below average. Streamline your checkout process!");

            if (tips.Count == 0)
                tips.Add("You're doing great! Keep maintaining high standards across all business areas.");

            return tips;
        }
    }

    public class LeaderboardEntry
    {
        public int BusinessId { get; set; }
        public int Rank { get; set; }
        public string BusinessName { get; set; } = string.Empty;
        public string BusinessType { get; set; } = string.Empty;
        public int TotalScore { get; set; }
        public int FinancialScore { get; set; }
        public int EfficiencyScore { get; set; }
        public int CivicScore { get; set; }
        public List<string> Tips { get; set; } = new List<string>();
    }
}
