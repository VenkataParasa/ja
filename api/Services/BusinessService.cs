using Microsoft.EntityFrameworkCore;
using JABizTown.API.Data;
using JABizTown.API.Models;

namespace JABizTown.API.Services
{
    public class BusinessService : IBusinessService
    {
        private readonly JABizTownDbContext _context;
        private readonly ILogger<BusinessService> _logger;

        public BusinessService(JABizTownDbContext context, ILogger<BusinessService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<IEnumerable<Business>> GetAllBusinessesAsync()
        {
            try
            {
                return await _context.Businesses
                    .Where(b => b.IsActive)
                    .Include(b => b.BankAccounts)
                    .Include(b => b.Students)
                    .ToListAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving all businesses");
                throw;
            }
        }

        public async Task<Business?> GetBusinessByIdAsync(int id)
        {
            try
            {
                return await _context.Businesses
                    .Include(b => b.BankAccounts)
                    .Include(b => b.Students)
                    .FirstOrDefaultAsync(b => b.BusinessId == id && b.IsActive);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving business with ID: {BusinessId}", id);
                throw;
            }
        }

        public async Task<Business> CreateBusinessAsync(Business business)
        {
            try
            {
                business.CreatedAt = DateTime.UtcNow;
                business.UpdatedAt = DateTime.UtcNow;
                business.IsActive = true;

                _context.Businesses.Add(business);
                await _context.SaveChangesAsync();

                _logger.LogInformation("Created new business: {BusinessName} with ID: {BusinessId}", business.BusinessName, business.BusinessId);
                return business;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating business: {BusinessName}", business.BusinessName);
                throw;
            }
        }

        public async Task<Business> UpdateBusinessAsync(int id, Business business)
        {
            try
            {
                var existingBusiness = await _context.Businesses.FindAsync(id);
                if (existingBusiness == null)
                {
                    throw new KeyNotFoundException($"Business with ID {id} not found");
                }

                existingBusiness.BusinessName = business.BusinessName;
                existingBusiness.BusinessType = business.BusinessType;
                existingBusiness.Description = business.Description;
                existingBusiness.UpdatedAt = DateTime.UtcNow;

                await _context.SaveChangesAsync();

                _logger.LogInformation("Updated business: {BusinessName} with ID: {BusinessId}", existingBusiness.BusinessName, existingBusiness.BusinessId);
                return existingBusiness;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating business with ID: {BusinessId}", id);
                throw;
            }
        }

        public async Task<bool> DeleteBusinessAsync(int id)
        {
            try
            {
                var business = await _context.Businesses.FindAsync(id);
                if (business == null)
                {
                    return false;
                }

                business.IsActive = false;
                business.UpdatedAt = DateTime.UtcNow;

                await _context.SaveChangesAsync();

                _logger.LogInformation("Soft deleted business: {BusinessName} with ID: {BusinessId}", business.BusinessName, business.BusinessId);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting business with ID: {BusinessId}", id);
                throw;
            }
        }

        public async Task<Business?> UpdateBusinessBalanceAsync(int id, decimal newBalance)
        {
            try
            {
                var business = await _context.Businesses.FindAsync(id);
                if (business == null)
                {
                    return null;
                }

                var oldBalance = business.CurrentBalance;
                business.CurrentBalance = newBalance;
                business.UpdatedAt = DateTime.UtcNow;

                await _context.SaveChangesAsync();

                _logger.LogInformation("Updated business balance from {OldBalance} to {NewBalance} for business ID: {BusinessId}", oldBalance, newBalance, id);
                return business;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating business balance for ID: {BusinessId}", id);
                throw;
            }
        }
    }
}
