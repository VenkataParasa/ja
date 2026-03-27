using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using System;
using System.Threading.Tasks;

namespace JABizTown.API.Data
{
    public class DbInitializer
    {
        private readonly IServiceProvider _serviceProvider;
        private readonly ILogger<DbInitializer> _logger;

        public DbInitializer(IServiceProvider serviceProvider, ILogger<DbInitializer> logger)
        {
            _serviceProvider = serviceProvider;
            _logger = logger;
        }

        public async Task InitializeAsync()
        {
            using var scope = _serviceProvider.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<JABizTownDbContext>();

            try
            {
                // Ensure database is created
                await context.Database.EnsureCreatedAsync();
                
                _logger.LogInformation("Database initialized successfully");

                // Seed initial data if tables are empty
                await SeedBusinessesAsync(context);
                await SeedRolesAsync(context);
                await context.SaveChangesAsync(); // Save prerequisite data

                await SeedBankAccountsAsync(context);
                await SeedStudentsAsync(context);
                await SeedSimulationStateAsync(context);
                
                await context.SaveChangesAsync();
                _logger.LogInformation("Database seeding completed successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "An error occurred while initializing the database");
                throw;
            }
        }

        private async Task SeedBusinessesAsync(JABizTownDbContext context)
        {
            if (await context.Businesses.AnyAsync())
            {
                _logger.LogInformation("Businesses table already contains data");
                return;
            }

            var businesses = new[]
            {
                new Models.Business
                {
                    BusinessName = "City Bank",
                    BusinessType = "Financial",
                    Description = "Provides banking services and manages accounts",
                    InitialCapital = 10000.00m,
                    CurrentBalance = 10000.00m,
                    LoanAmount = 10000.00m,
                    LoanPaid = 8000.00m,
                    Revenue = 15000.00m,
                    PhilanthropicTotal = 500.00m,
                    EfficiencyScore = 95.0,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Models.Business
                {
                    BusinessName = "Tech Solutions",
                    BusinessType = "Technology",
                    Description = "Software development and IT services",
                    InitialCapital = 8000.00m,
                    CurrentBalance = 8000.00m,
                    LoanAmount = 8000.00m,
                    LoanPaid = 4000.00m,
                    Revenue = 12000.00m,
                    PhilanthropicTotal = 200.00m,
                    EfficiencyScore = 80.0,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Models.Business
                {
                    BusinessName = "Healthy Foods Market",
                    BusinessType = "Retail",
                    Description = "Grocery store and food products",
                    InitialCapital = 6000.00m,
                    CurrentBalance = 6000.00m,
                    LoanAmount = 6000.00m,
                    LoanPaid = 6000.00m,
                    Revenue = 10000.00m,
                    PhilanthropicTotal = 300.00m,
                    EfficiencyScore = 90.0,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Models.Business
                {
                    BusinessName = "Construction Co",
                    BusinessType = "Construction",
                    Description = "Building and construction services",
                    InitialCapital = 7500.00m,
                    CurrentBalance = 7500.00m,
                    LoanAmount = 7500.00m,
                    LoanPaid = 3750.00m,
                    Revenue = 9000.00m,
                    PhilanthropicTotal = 150.00m,
                    EfficiencyScore = 75.0,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Models.Business
                {
                    BusinessName = "Energy Plus",
                    BusinessType = "Utilities",
                    Description = "Electric and utility services",
                    InitialCapital = 9000.00m,
                    CurrentBalance = 9000.00m,
                    LoanAmount = 9000.00m,
                    LoanPaid = 4500.00m,
                    Revenue = 11000.00m,
                    PhilanthropicTotal = 250.00m,
                    EfficiencyScore = 85.0,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Models.Business
                {
                    BusinessName = "Media Hub",
                    BusinessType = "Media",
                    Description = "Advertising and media production",
                    InitialCapital = 5500.00m,
                    CurrentBalance = 5500.00m,
                    LoanAmount = 5500.00m,
                    LoanPaid = 5500.00m,
                    Revenue = 8500.00m,
                    PhilanthropicTotal = 400.00m,
                    EfficiencyScore = 92.0,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Models.Business
                {
                    BusinessName = "Healthcare Center",
                    BusinessType = "Healthcare",
                    Description = "Medical and health services",
                    InitialCapital = 8500.00m,
                    CurrentBalance = 8500.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Models.Business
                {
                    BusinessName = "Education Academy",
                    BusinessType = "Education",
                    Description = "Training and educational services",
                    InitialCapital = 7000.00m,
                    CurrentBalance = 7000.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                }
            };

            await context.Businesses.AddRangeAsync(businesses);
            _logger.LogInformation("Seeded {Count} businesses", businesses.Length);
        }

        private async Task SeedRolesAsync(JABizTownDbContext context)
        {
            if (await context.Roles.AnyAsync())
            {
                _logger.LogInformation("Roles table already contains data");
                return;
            }

            var roles = new[]
            {
                new Models.Role
                {
                    RoleName = "CEO",
                    RoleDescription = "Chief Executive Officer",
                    BaseSalary = 500.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Manager",
                    RoleDescription = "Department Manager",
                    BaseSalary = 350.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Accountant",
                    RoleDescription = "Financial Accountant",
                    BaseSalary = 300.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Developer",
                    RoleDescription = "Software Developer",
                    BaseSalary = 280.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Cashier",
                    RoleDescription = "Bank Cashier",
                    BaseSalary = 200.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Sales Associate",
                    RoleDescription = "Sales Representative",
                    BaseSalary = 220.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Engineer",
                    RoleDescription = "Technical Engineer",
                    BaseSalary = 320.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Marketing Specialist",
                    RoleDescription = "Marketing Coordinator",
                    BaseSalary = 250.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Doctor",
                    RoleDescription = "Medical Doctor",
                    BaseSalary = 450.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                },
                new Models.Role
                {
                    RoleName = "Teacher",
                    RoleDescription = "Education Instructor",
                    BaseSalary = 275.00m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow
                }
            };

            await context.Roles.AddRangeAsync(roles);
            _logger.LogInformation("Seeded {Count} roles", roles.Length);
        }

        private async Task SeedBankAccountsAsync(JABizTownDbContext context)
        {
            if (await context.BankAccounts.AnyAsync())
            {
                _logger.LogInformation("BankAccounts table already contains data");
                return;
            }

            var businesses = await context.Businesses.ToListAsync();
            var bankAccounts = new List<Models.BankAccount>();

            foreach (var business in businesses)
            {
                bankAccounts.Add(new Models.BankAccount
                {
                    AccountNumber = $"BIZ{business.BusinessId:D3}",
                    AccountHolderName = business.BusinessName,
                    BusinessId = business.BusinessId,
                    Balance = business.CurrentBalance,
                    AccountType = "Business",
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                });
            }

            await context.BankAccounts.AddRangeAsync(bankAccounts);
            _logger.LogInformation("Seeded {Count} bank accounts", bankAccounts.Count);
        }

        private async Task SeedStudentsAsync(JABizTownDbContext context)
        {
            if (await context.Students.AnyAsync())
            {
                _logger.LogInformation("Students table already contains data");
                return;
            }

            var businesses = await context.Businesses.ToListAsync();
            var roles = await context.Roles.ToListAsync();
            
            if (businesses.Count < 5 || roles.Count < 5)
            {
                _logger.LogWarning("Cannot seed students: Businesses or Roles are missing or insufficient");
                return;
            }

            var students = new List<Models.Student>
            {
                new Models.Student { FirstName = "Alex", LastName = "Johnson", Email = "alex.j@biztown.edu", StudentNumber = "STU001", BusinessId = businesses[0].BusinessId, RoleId = roles[0].RoleId },
                new Models.Student { FirstName = "Maria", LastName = "Garcia", Email = "m.garcia@biztown.edu", StudentNumber = "STU002", BusinessId = businesses[0].BusinessId, RoleId = roles[2].RoleId },
                new Models.Student { FirstName = "Kenji", LastName = "Sato", Email = "k.sato@biztown.edu", StudentNumber = "STU003", BusinessId = businesses[1].BusinessId, RoleId = roles[0].RoleId },
                new Models.Student { FirstName = "Elena", LastName = "Petrov", Email = "e.petrov@biztown.edu", StudentNumber = "STU004", BusinessId = businesses[1].BusinessId, RoleId = roles[3].RoleId },
                new Models.Student { FirstName = "David", LastName = "Kim", Email = "d.kim@biztown.edu", StudentNumber = "STU005", BusinessId = businesses[2].BusinessId, RoleId = roles[0].RoleId },
                new Models.Student { FirstName = "Aisha", LastName = "Bello", Email = "a.bello@biztown.edu", StudentNumber = "STU006", BusinessId = businesses[2].BusinessId, RoleId = roles[5].RoleId },
                new Models.Student { FirstName = "Lucas", LastName = "Muller", Email = "l.muller@biztown.edu", StudentNumber = "STU007", BusinessId = businesses[3].BusinessId, RoleId = roles[0].RoleId },
                new Models.Student { FirstName = "Sofia", LastName = "Bianchi", Email = "s.bianchi@biztown.edu", StudentNumber = "STU008", BusinessId = businesses[4].BusinessId, RoleId = roles[0].RoleId },
                new Models.Student { FirstName = "Ryan", LastName = "Thompson", Email = "r.thompson@biztown.edu", StudentNumber = "STU009", BusinessId = businesses[5].BusinessId, RoleId = roles[0].RoleId },
                new Models.Student { FirstName = "Zoe", LastName = "Chen", Email = "z.chen@biztown.edu", StudentNumber = "STU010", BusinessId = businesses[6].BusinessId, RoleId = roles[0].RoleId }
            };

            var personalAccounts = new List<Models.BankAccount>();
            for (var i = 0; i < students.Count; i++)
            {
                personalAccounts.Add(new Models.BankAccount
                {
                    AccountNumber = $"STU{i + 1:D3}",
                    AccountHolderName = $"{students[i].FirstName} {students[i].LastName}",
                    AccountType = "Personal",
                    Balance = 0m,
                    IsActive = true,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                });
            }

            await context.BankAccounts.AddRangeAsync(personalAccounts);
            await context.SaveChangesAsync();

            for (var i = 0; i < students.Count; i++)
            {
                students[i].BankAccountId = personalAccounts[i].AccountId;
            }

            await context.Students.AddRangeAsync(students);
            _logger.LogInformation("Seeded {Count} students", students.Count);
        }

        private async Task SeedSimulationStateAsync(JABizTownDbContext context)
        {
            if (await context.SimulationStates.AnyAsync())
            {
                return;
            }

            var state = new Models.SimulationState
            {
                Status = "Active",
                IsTornadoActive = false,
                ActiveIncident = "None",
                IncidentMessage = string.Empty,
                XPData = "{}",
                ContributionData = "{}",
                UpdatedAt = DateTime.UtcNow
            };

            await context.SimulationStates.AddAsync(state);
            _logger.LogInformation("Seeded initial simulation state");
        }
    }
}
