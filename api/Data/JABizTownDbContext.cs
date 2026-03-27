using Microsoft.EntityFrameworkCore;
using JABizTown.API.Models;

namespace JABizTown.API.Data
{
    public class JABizTownDbContext : DbContext
    {
        public JABizTownDbContext(DbContextOptions<JABizTownDbContext> options) : base(options)
        {
        }

        public DbSet<Business> Businesses { get; set; }
        public DbSet<BankAccount> BankAccounts { get; set; }
        public DbSet<Role> Roles { get; set; }
        public DbSet<Student> Students { get; set; }
        public DbSet<Transaction> Transactions { get; set; }
        public DbSet<SimulationState> SimulationStates { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure Business entity
            modelBuilder.Entity<Business>(entity =>
            {
                entity.HasKey(e => e.BusinessId);
                entity.Property(e => e.BusinessName).IsRequired().HasMaxLength(100);
                entity.Property(e => e.BusinessType).IsRequired().HasMaxLength(50);
                entity.Property(e => e.Description).HasMaxLength(500);
                entity.Property(e => e.InitialCapital).HasColumnType("decimal(18,2)");
                entity.Property(e => e.CurrentBalance).HasColumnType("decimal(18,2)");
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("GETUTCDATE()");
                entity.Property(e => e.UpdatedAt).HasDefaultValueSql("GETUTCDATE()");
            });

            // Configure BankAccount entity
            modelBuilder.Entity<BankAccount>(entity =>
            {
                entity.HasKey(e => e.AccountId);
                entity.Property(e => e.AccountNumber).IsRequired().HasMaxLength(20);
                entity.Property(e => e.AccountHolderName).IsRequired().HasMaxLength(100);
                entity.Property(e => e.Balance).HasColumnType("decimal(18,2)");
                entity.Property(e => e.AccountType).IsRequired().HasMaxLength(20).HasDefaultValue("Checking");
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("GETUTCDATE()");
                entity.Property(e => e.UpdatedAt).HasDefaultValueSql("GETUTCDATE()");
                
                entity.HasOne(e => e.Business)
                    .WithMany(b => b.BankAccounts)
                    .HasForeignKey(e => e.BusinessId)
                    .OnDelete(DeleteBehavior.SetNull);
            });

            // Configure Role entity
            modelBuilder.Entity<Role>(entity =>
            {
                entity.HasKey(e => e.RoleId);
                entity.Property(e => e.RoleName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.RoleDescription).HasMaxLength(200);
                entity.Property(e => e.BaseSalary).HasColumnType("decimal(18,2)");
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("GETUTCDATE()");
            });

            // Configure Student entity
            modelBuilder.Entity<Student>(entity =>
            {
                entity.HasKey(e => e.StudentId);
                entity.Property(e => e.FirstName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.LastName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.Email).HasMaxLength(100);
                entity.Property(e => e.StudentNumber).HasMaxLength(20);
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("GETUTCDATE()");
                
                entity.HasOne(e => e.Business)
                    .WithMany(b => b.Students)
                    .HasForeignKey(e => e.BusinessId)
                    .OnDelete(DeleteBehavior.SetNull);
                    
                entity.HasOne(e => e.Role)
                    .WithMany(r => r.Students)
                    .HasForeignKey(e => e.RoleId)
                    .OnDelete(DeleteBehavior.SetNull);
                    
                entity.HasOne(e => e.BankAccount)
                    .WithMany(ba => ba.Students)
                    .HasForeignKey(e => e.BankAccountId)
                    .OnDelete(DeleteBehavior.SetNull);
            });

            // Configure Transaction entity
            modelBuilder.Entity<Transaction>(entity =>
            {
                entity.HasKey(e => e.TransactionId);
                entity.Property(e => e.Amount).HasColumnType("decimal(18,2)");
                entity.Property(e => e.TransactionType).IsRequired().HasMaxLength(20);
                entity.Property(e => e.Description).HasMaxLength(200);
                entity.Property(e => e.TransactionDate).HasDefaultValueSql("GETUTCDATE()");
                
                entity.HasOne(e => e.FromAccount)
                    .WithMany(ba => ba.FromTransactions)
                    .HasForeignKey(e => e.FromAccountId)
                    .OnDelete(DeleteBehavior.Restrict);
                    
                entity.HasOne(e => e.ToAccount)
                    .WithMany(ba => ba.ToTransactions)
                    .HasForeignKey(e => e.ToAccountId)
                    .OnDelete(DeleteBehavior.Restrict);
                    
                entity.HasOne(e => e.Business)
                    .WithMany(b => b.Transactions)
                    .HasForeignKey(e => e.BusinessId)
                    .OnDelete(DeleteBehavior.SetNull);
                    
                entity.HasOne(e => e.Student)
                    .WithMany(s => s.Transactions)
                    .HasForeignKey(e => e.StudentId)
                    .OnDelete(DeleteBehavior.SetNull);
            });

            // Create indexes for better performance
            modelBuilder.Entity<Transaction>()
                .HasIndex(e => e.TransactionDate)
                .HasDatabaseName("IX_Transactions_TransactionDate");
                
            modelBuilder.Entity<Transaction>()
                .HasIndex(e => e.BusinessId)
                .HasDatabaseName("IX_Transactions_BusinessId");
                
            modelBuilder.Entity<Student>()
                .HasIndex(e => e.BusinessId)
                .HasDatabaseName("IX_Students_BusinessId");
                
            modelBuilder.Entity<BankAccount>()
                .HasIndex(e => e.BusinessId)
                .HasDatabaseName("IX_BankAccounts_BusinessId");

            // Configure SimulationState
            modelBuilder.Entity<SimulationState>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Status).HasDefaultValue("Active");
                entity.Property(e => e.UpdatedAt).HasDefaultValueSql("GETUTCDATE()");
            });
        }
    }
}
