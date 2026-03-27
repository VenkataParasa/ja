using Microsoft.AspNetCore.Mvc;
using JABizTown.API.Models;
using JABizTown.API.Services;

namespace JABizTown.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BankAccountsController : ControllerBase
    {
        private readonly IBankAccountService _bankAccountService;
        private readonly ILogger<BankAccountsController> _logger;

        public BankAccountsController(IBankAccountService bankAccountService, ILogger<BankAccountsController> logger)
        {
            _bankAccountService = bankAccountService;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<BankAccount>>> GetBankAccounts()
        {
            try
            {
                var accounts = await _bankAccountService.GetAllBankAccountsAsync();
                return Ok(accounts);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving bank accounts");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<BankAccount>> GetBankAccount(int id)
        {
            try
            {
                var account = await _bankAccountService.GetBankAccountByIdAsync(id);
                if (account == null)
                {
                    return NotFound();
                }
                return Ok(account);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving bank account with ID: {AccountId}", id);
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPost]
        public async Task<ActionResult<BankAccount>> CreateBankAccount(BankAccount bankAccount)
        {
            try
            {
                var createdAccount = await _bankAccountService.CreateBankAccountAsync(bankAccount);
                return CreatedAtAction(nameof(GetBankAccount), new { id = createdAccount.AccountId }, createdAccount);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating bank account");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPut("{id}/balance")]
        public async Task<ActionResult<BankAccount>> UpdateBalance(int id, [FromBody] decimal newBalance)
        {
            try
            {
                var account = await _bankAccountService.UpdateAccountBalanceAsync(id, newBalance);
                if (account == null)
                {
                    return NotFound();
                }
                return Ok(account);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating balance for account ID: {AccountId}", id);
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBankAccount(int id)
        {
            try
            {
                var result = await _bankAccountService.DeleteBankAccountAsync(id);
                if (!result)
                {
                    return NotFound();
                }
                return NoContent();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting bank account with ID: {AccountId}", id);
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpGet("business/{businessId}")]
        public async Task<ActionResult<IEnumerable<BankAccount>>> GetAccountsByBusiness(int businessId)
        {
            try
            {
                var accounts = await _bankAccountService.GetAccountsByBusinessIdAsync(businessId);
                return Ok(accounts);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving accounts for business ID: {BusinessId}", businessId);
                return StatusCode(500, "Internal server error");
            }
        }
    }
}
