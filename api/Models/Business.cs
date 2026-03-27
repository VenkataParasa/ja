using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace JABizTown.API.Models
{
    public class Business
    {
        [Key]
        public int BusinessId { get; set; }

        [Required]
        [MaxLength(100)]
        public string BusinessName { get; set; } = string.Empty;

        [Required]
        [MaxLength(50)]
        public string BusinessType { get; set; } = string.Empty;

        [MaxLength(500)]
        public string? Description { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal InitialCapital { get; set; } = 5000.00m;

        [Column(TypeName = "decimal(18,2)")]
        public decimal CurrentBalance { get; set; } = 5000.00m;

        [Column(TypeName = "decimal(18,2)")]
        public decimal LoanAmount { get; set; } = 5000.00m;

        [Column(TypeName = "decimal(18,2)")]
        public decimal LoanPaid { get; set; } = 0.00m;

        [Column(TypeName = "decimal(18,2)")]
        public decimal Revenue { get; set; } = 0.00m;

        [Column(TypeName = "decimal(18,2)")]
        public decimal PhilanthropicTotal { get; set; } = 0.00m;

        public double EfficiencyScore { get; set; } = 100.0;

        public bool IsActive { get; set; } = true;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

        // Navigation properties
        public virtual ICollection<BankAccount> BankAccounts { get; set; } = new List<BankAccount>();
        public virtual ICollection<Student> Students { get; set; } = new List<Student>();
        public virtual ICollection<Transaction> Transactions { get; set; } = new List<Transaction>();
    }
}
