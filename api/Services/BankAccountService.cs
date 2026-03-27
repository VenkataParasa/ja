using Microsoft.EntityFrameworkCore;
using JABizTown.API.Data;
using JABizTown.API.Models;

namespace JABizTown.API.Services
{
    public class BankAccountService : IBankAccountService
    {
        private readonly JABizTownDbContext _context;
        private readonly ILogger<BankAccountService> _logger;

        public BankAccountService(JABizTownDbContext context, ILogger<BankAccountService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<IEnumerable<BankAccount>> GetAllBankAccountsAsync()
        {
            try
            {
                return await _context.BankAccounts
                    .Where(ba => ba.IsActive)
                    .Include(ba => ba.Business)
                    .Include(ba => ba.Students)
                    .ToListAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving all bank accounts");
                throw;
            }
        }

        public async Task<BankAccount?> GetBankAccountByIdAsync(int id)
        {
            try
            {
                return await _context.BankAccounts
                    .Include(ba => ba.Business)
                    .Include(ba => ba.Students)
                    .FirstOrDefaultAsync(ba => ba.AccountId == id && ba.IsActive);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving bank account with ID: {AccountId}", id);
                throw;
            }
        }

        public async Task<BankAccount> CreateBankAccountAsync(BankAccount bankAccount)
        {
            try
            {
                bankAccount.CreatedAt = DateTime.UtcNow;
                bankAccount.UpdatedAt = DateTime.UtcNow;
                bankAccount.IsActive = true;

                _context.BankAccounts.Add(bankAccount);
                await _context.SaveChangesAsync();

                _logger.LogInformation("Created new bank account: {AccountNumber} for {AccountHolderName}", bankAccount.AccountNumber, bankAccount.AccountHolderName);
                return bankAccount;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating bank account: {AccountNumber}", bankAccount.AccountNumber);
                throw;
            }
        }

        public async Task<BankAccount?> UpdateAccountBalanceAsync(int id, decimal newBalance)
        {
            try
            {
                var account = await _context.BankAccounts.FindAsync(id);
                if (account == null)
                {
                    return null;
                }

                var oldBalance = account.Balance;
                account.Balance = newBalance;
                account.UpdatedAt = DateTime.UtcNow;

                await _context.SaveChangesAsync();

                _logger.LogInformation("Updated account balance from {OldBalance} to {NewBalance} for account ID: {AccountId}", oldBalance, newBalance, id);
                return account;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating account balance for ID: {AccountId}", id);
                throw;
            }
        }

        public async Task<bool> DeleteBankAccountAsync(int id)
        {
            try
            {
                var account = await _context.BankAccounts.FindAsync(id);
                if (account == null)
                {
                    return false;
                }

                account.IsActive = false;
                account.UpdatedAt = DateTime.UtcNow;

                await _context.SaveChangesAsync();

                _logger.LogInformation("Soft deleted bank account: {AccountNumber} with ID: {AccountId}", account.AccountNumber, account.AccountId);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting bank account with ID: {AccountId}", id);
                throw;
            }
        }

        public async Task<IEnumerable<BankAccount>> GetAccountsByBusinessIdAsync(int businessId)
        {
            try
            {
                return await _context.BankAccounts
                    .Where(ba => ba.BusinessId == businessId && ba.IsActive)
                    .Include(ba => ba.Business)
                    .ToListAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving bank accounts for business ID: {BusinessId}", businessId);
                throw;
            }
        }
    }
}
