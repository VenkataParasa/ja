using JABizTown.API.Models;

namespace JABizTown.API.Services
{
    public interface ITransactionService
    {
        Task<IEnumerable<Transaction>> GetAllTransactionsAsync();
        Task<Transaction?> GetTransactionByIdAsync(int id);
        Task<Transaction> CreateTransactionAsync(Transaction transaction);
        Task<IEnumerable<Transaction>> GetTransactionsByBusinessIdAsync(int businessId);
        Task<IEnumerable<Transaction>> GetTransactionsByAccountIdAsync(int accountId);
        Task<bool> ProcessTransferAsync(int fromAccountId, int toAccountId, decimal amount, string description);
    }
}
