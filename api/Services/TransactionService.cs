using Microsoft.EntityFrameworkCore;
using JABizTown.API.Data;
using JABizTown.API.Models;

namespace JABizTown.API.Services
{
    public class TransactionService : ITransactionService
    {
        private readonly JABizTownDbContext _context;
        private readonly IBankAccountService _bankAccountService;
        private readonly ILogger<TransactionService> _logger;

        public TransactionService(
            JABizTownDbContext context, 
            IBankAccountService bankAccountService,
            ILogger<TransactionService> logger)
        {
            _context = context;
            _bankAccountService = bankAccountService;
            _logger = logger;
        }

        public async Task<IEnumerable<Transaction>> GetAllTransactionsAsync()
        {
            try
            {
                return await _context.Transactions
                    .Include(t => t.FromAccount)
                    .Include(t => t.ToAccount)
                    .Include(t => t.Business)
                    .Include(t => t.Student)
                    .OrderByDescending(t => t.TransactionDate)
                    .ToListAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving all transactions");
                throw;
            }
        }

        public async Task<Transaction?> GetTransactionByIdAsync(int id)
        {
            try
            {
                return await _context.Transactions
                    .Include(t => t.FromAccount)
                    .Include(t => t.ToAccount)
                    .Include(t => t.Business)
                    .Include(t => t.Student)
                    .FirstOrDefaultAsync(t => t.TransactionId == id);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving transaction with ID: {TransactionId}", id);
                throw;
            }
        }

        public async Task<Transaction> CreateTransactionAsync(Transaction transaction)
        {
            using var transactionScope = await _context.Database.BeginTransactionAsync();
            try
            {
                transaction.TransactionDate = DateTime.UtcNow;

                // Process the transaction based on type
                if (transaction.TransactionType == "Transfer" && transaction.FromAccountId.HasValue && transaction.ToAccountId.HasValue)
                {
                    await ProcessTransferInternal(transaction.FromAccountId.Value, transaction.ToAccountId.Value, transaction.Amount, transaction.Description);
                }
                else if (transaction.TransactionType == "Deposit" && transaction.ToAccountId.HasValue)
                {
                    await ProcessDepositInternal(transaction.ToAccountId.Value, transaction.Amount);
                }
                else if (transaction.TransactionType == "Withdrawal" && transaction.FromAccountId.HasValue)
                {
                    await ProcessWithdrawalInternal(transaction.FromAccountId.Value, transaction.Amount);
                }

                _context.Transactions.Add(transaction);
                await _context.SaveChangesAsync();
                await transactionScope.CommitAsync();

                _logger.LogInformation("Created transaction: {TransactionType} of amount {Amount} with ID: {TransactionId}", 
                    transaction.TransactionType, transaction.Amount, transaction.TransactionId);
                
                return transaction;
            }
            catch (Exception ex)
            {
                await transactionScope.RollbackAsync();
                _logger.LogError(ex, "Error creating transaction");
                throw;
            }
        }

        public async Task<IEnumerable<Transaction>> GetTransactionsByBusinessIdAsync(int businessId)
        {
            try
            {
                return await _context.Transactions
                    .Where(t => t.BusinessId == businessId)
                    .Include(t => t.FromAccount)
                    .Include(t => t.ToAccount)
                    .OrderByDescending(t => t.TransactionDate)
                    .ToListAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving transactions for business ID: {BusinessId}", businessId);
                throw;
            }
        }

        public async Task<IEnumerable<Transaction>> GetTransactionsByAccountIdAsync(int accountId)
        {
            try
            {
                return await _context.Transactions
                    .Where(t => t.FromAccountId == accountId || t.ToAccountId == accountId)
                    .Include(t => t.FromAccount)
                    .Include(t => t.ToAccount)
                    .OrderByDescending(t => t.TransactionDate)
                    .ToListAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving transactions for account ID: {AccountId}", accountId);
                throw;
            }
        }

        public async Task<bool> ProcessTransferAsync(int fromAccountId, int toAccountId, decimal amount, string description)
        {
            using var transactionScope = await _context.Database.BeginTransactionAsync();
            try
            {
                var result = await ProcessTransferInternal(fromAccountId, toAccountId, amount, description ?? string.Empty);
                await transactionScope.CommitAsync();
                return result;
            }
            catch (Exception ex)
            {
                await transactionScope.RollbackAsync();
                _logger.LogError(ex, "Error processing transfer from account {FromAccountId} to account {ToAccountId}", fromAccountId, toAccountId);
                throw;
            }
        }

        private async Task<bool> ProcessTransferInternal(int fromAccountId, int toAccountId, decimal amount, string description)
        {
            // Get accounts
            var fromAccount = await _bankAccountService.GetBankAccountByIdAsync(fromAccountId);
            var toAccount = await _bankAccountService.GetBankAccountByIdAsync(toAccountId);

            if (fromAccount == null || toAccount == null)
            {
                throw new ArgumentException("One or both accounts not found");
            }

            if (fromAccount.Balance < amount)
            {
                throw new InvalidOperationException("Insufficient funds in source account");
            }

            // Update balances
            await _bankAccountService.UpdateAccountBalanceAsync(fromAccountId, fromAccount.Balance - amount);
            await _bankAccountService.UpdateAccountBalanceAsync(toAccountId, toAccount.Balance + amount);

            // Create transaction record
            var transaction = new Transaction
            {
                FromAccountId = fromAccountId,
                ToAccountId = toAccountId,
                Amount = amount,
                TransactionType = "Transfer",
                Description = description,
                TransactionDate = DateTime.UtcNow
            };

            _context.Transactions.Add(transaction);
            await _context.SaveChangesAsync();

            _logger.LogInformation("Processed transfer of {Amount} from account {FromAccountId} to account {ToAccountId}", 
                amount, fromAccountId, toAccountId);

            return true;
        }

        private async Task<bool> ProcessDepositInternal(int accountId, decimal amount)
        {
            var account = await _bankAccountService.GetBankAccountByIdAsync(accountId);
            if (account == null)
            {
                throw new ArgumentException("Account not found");
            }

            await _bankAccountService.UpdateAccountBalanceAsync(accountId, account.Balance + amount);
            return true;
        }

        private async Task<bool> ProcessWithdrawalInternal(int accountId, decimal amount)
        {
            var account = await _bankAccountService.GetBankAccountByIdAsync(accountId);
            if (account == null)
            {
                throw new ArgumentException("Account not found");
            }

            if (account.Balance < amount)
            {
                throw new InvalidOperationException("Insufficient funds");
            }

            await _bankAccountService.UpdateAccountBalanceAsync(accountId, account.Balance - amount);
            return true;
        }
    }
}
