using JABizTown.API.Models;

namespace JABizTown.API.Services
{
    public interface IBusinessService
    {
        Task<IEnumerable<Business>> GetAllBusinessesAsync();
        Task<Business?> GetBusinessByIdAsync(int id);
        Task<Business> CreateBusinessAsync(Business business);
        Task<Business> UpdateBusinessAsync(int id, Business business);
        Task<bool> DeleteBusinessAsync(int id);
        Task<Business?> UpdateBusinessBalanceAsync(int id, decimal newBalance);
    }
}
