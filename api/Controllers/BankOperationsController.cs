using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using JABizTown.API.Data;
using JABizTown.API.Models;

namespace JABizTown.API.Controllers
{
    [ApiController]
    [Route("api/bank")]
    public class BankOperationsController : ControllerBase
    {
        private readonly JABizTownDbContext _context;
        private readonly ILogger<BankOperationsController> _logger;

        public BankOperationsController(JABizTownDbContext context, ILogger<BankOperationsController> logger)
        {
            _context = context;
            _logger = logger;
        }

        [HttpPost("deposit-paycheck")]
        public async Task<IActionResult> DepositPaycheck([FromBody] PaycheckRequest request)
        {
            var student = await _context.Students
                .Include(s => s.BankAccount)
                .FirstOrDefaultAsync(s => s.StudentId == request.StudentId);

            if (student == null) return NotFound("Student not found");
            if (request.Amount <= 0) return BadRequest("Amount must be greater than zero");

            if (student.BankAccount == null)
            {
                student.BankAccount = new BankAccount
                {
                    AccountNumber = $"STU{student.StudentId:D4}",
                    AccountHolderName = $"{student.FirstName} {student.LastName}",
                    AccountType = "Personal",
                    Balance = 0m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                };
                _context.BankAccounts.Add(student.BankAccount);
                await _context.SaveChangesAsync();
                student.BankAccountId = student.BankAccount.AccountId;
            }

            student.BankAccount.Balance += request.Amount;
            student.BankAccount.UpdatedAt = DateTime.UtcNow;

            var transaction = new Transaction
            {
                ToAccountId = student.BankAccount.AccountId,
                Amount = request.Amount,
                TransactionType = "Deposit",
                Description = "Paycheck Deposit",
                TransactionDate = DateTime.UtcNow
            };

            _context.Transactions.Add(transaction);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                message = "Paycheck deposited",
                newBalance = student.BankAccount.Balance,
                accountId = student.BankAccount.AccountId,
                studentId = student.StudentId
            });
        }

        [HttpPost("apply-loan")]
        public async Task<IActionResult> ApplyLoan([FromBody] LoanRequest request)
        {
            if (request.Amount <= 0) return BadRequest("Amount must be greater than zero");

            var business = await _context.Businesses.FindAsync(request.BusinessId);
            if (business == null) return NotFound("Business not found");

            if (request.StudentId.HasValue)
            {
                var requestingStudent = await _context.Students
                    .Include(s => s.Role)
                    .FirstOrDefaultAsync(s => s.StudentId == request.StudentId.Value);

                if (requestingStudent == null) return NotFound("Requesting student not found");
                if (requestingStudent.BusinessId != request.BusinessId) return BadRequest("Student does not belong to this business");

                var roleName = requestingStudent.Role?.RoleName ?? string.Empty;
                var canRequestLoan = roleName.Equals("CEO", StringComparison.OrdinalIgnoreCase) ||
                                     roleName.Equals("CFO", StringComparison.OrdinalIgnoreCase);
                if (!canRequestLoan) return Forbid("Only CEO or CFO can request a business loan");
            }

            business.LoanAmount += request.Amount;
            business.CurrentBalance += request.Amount;
            business.UpdatedAt = DateTime.UtcNow;

            // Find business bank account
            var businessAccount = await _context.BankAccounts.FirstOrDefaultAsync(b => b.BusinessId == business.BusinessId);
            if (businessAccount != null)
            {
                businessAccount.Balance += request.Amount;
                
                var transaction = new Transaction
                {
                    ToAccountId = businessAccount.AccountId,
                    Amount = request.Amount,
                    TransactionType = "Loan",
                    Description = "Business Loan Approved",
                    TransactionDate = DateTime.UtcNow
                };
                _context.Transactions.Add(transaction);
            }

            await _context.SaveChangesAsync();
            return Ok(new { message = "Loan approved", newBalance = business.CurrentBalance, newLoanAmount = business.LoanAmount });
        }

        [HttpPost("donate")]
        public async Task<IActionResult> Donate([FromBody] DonateRequest request)
        {
            var business = await _context.Businesses.FindAsync(request.BusinessId);
            if (business == null) return NotFound("Business not found");
            if (request.Amount <= 0) return BadRequest("Amount must be greater than zero");

            if (business.CurrentBalance < request.Amount) return BadRequest("Insufficient funds");

            business.CurrentBalance -= request.Amount;
            business.PhilanthropicTotal += request.Amount;
            business.UpdatedAt = DateTime.UtcNow;

            var charityAccount = await _context.BankAccounts.FirstOrDefaultAsync(a => a.AccountType == "System Charity");
            if (charityAccount == null)
            {
                charityAccount = new BankAccount
                {
                    AccountNumber = "SYS-CHARITY",
                    AccountHolderName = "JA BizTown Charity Fund",
                    AccountType = "System Charity",
                    Balance = 0m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                };
                _context.BankAccounts.Add(charityAccount);
                await _context.SaveChangesAsync();
            }
            charityAccount.Balance += request.Amount;
            charityAccount.UpdatedAt = DateTime.UtcNow;

            var businessAccount = await _context.BankAccounts.FirstOrDefaultAsync(b => b.BusinessId == business.BusinessId);
            if (businessAccount != null)
            {
                businessAccount.Balance -= request.Amount;
                var transaction = new Transaction
                {
                    FromAccountId = businessAccount.AccountId,
                    ToAccountId = charityAccount.AccountId,
                    Amount = request.Amount,
                    TransactionType = "Donation",
                    Description = "Charitable Donation to JA BizTown Fund",
                    TransactionDate = DateTime.UtcNow
                };
                _context.Transactions.Add(transaction);
            }

            await _context.SaveChangesAsync();
            return Ok(new { message = "Donation successful", newBalance = business.CurrentBalance });
        }

        [HttpPost("pos-sale")]
        public async Task<IActionResult> ProcessStorefrontSale([FromBody] PosSaleRequest request)
        {
            var business = await _context.Businesses.FindAsync(request.BusinessId);
            if (business == null) return NotFound("Business not found");
            if (request.Amount <= 0) return BadRequest("Amount must be greater than zero");

            // For POS, we'll simulate money coming from a "System Customer" directly into the business
            business.CurrentBalance += request.Amount;
            business.Revenue += request.Amount;
            business.UpdatedAt = DateTime.UtcNow;

            var businessAccount = await _context.BankAccounts.FirstOrDefaultAsync(b => b.BusinessId == business.BusinessId);
            if (businessAccount != null)
            {
                businessAccount.Balance += request.Amount;
                
                var transaction = new Transaction
                {
                    ToAccountId = businessAccount.AccountId,
                    Amount = request.Amount,
                    TransactionType = "Sale",
                    Description = string.IsNullOrWhiteSpace(request.ItemName) ? "Storefront Sale (POS)" : $"Storefront Sale: {request.ItemName}",
                    TransactionDate = DateTime.UtcNow
                };
                _context.Transactions.Add(transaction);
            }

            // Gamification: Processing sales increases EfficiencyScore dynamically (simplified logic)
            if (business.EfficiencyScore < 100)
            {
                business.EfficiencyScore = Math.Min(100, business.EfficiencyScore + 1);
            }

            await _context.SaveChangesAsync();
            return Ok(new { message = "Sale processed", newBalance = business.CurrentBalance });
        }
    }

    public class PaycheckRequest
    {
        public int StudentId { get; set; }
        public decimal Amount { get; set; }
    }

    public class LoanRequest
    {
        public int BusinessId { get; set; }
        public decimal Amount { get; set; }
        public int? StudentId { get; set; }
    }

    public class DonateRequest
    {
        public int BusinessId { get; set; }
        public decimal Amount { get; set; }
    }

    public class PosSaleRequest
    {
        public int BusinessId { get; set; }
        public decimal Amount { get; set; }
        public string? ItemName { get; set; }
    }
}
