using JABizTown.API.Models;

namespace JABizTown.API.Services
{
    public interface IBankAccountService
    {
        Task<IEnumerable<BankAccount>> GetAllBankAccountsAsync();
        Task<BankAccount?> GetBankAccountByIdAsync(int id);
        Task<BankAccount> CreateBankAccountAsync(BankAccount bankAccount);
        Task<BankAccount?> UpdateAccountBalanceAsync(int id, decimal newBalance);
        Task<bool> DeleteBankAccountAsync(int id);
        Task<IEnumerable<BankAccount>> GetAccountsByBusinessIdAsync(int businessId);
    }
}
