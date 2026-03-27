using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace JABizTown.API.Models
{
    public class BankAccount
    {
        [Key]
        public int AccountId { get; set; }

        [Required]
        [MaxLength(20)]
        [Column(TypeName = "nvarchar(20)")]
        public string AccountNumber { get; set; } = string.Empty;

        [Required]
        [MaxLength(100)]
        public string AccountHolderName { get; set; } = string.Empty;

        public int? BusinessId { get; set; }

        [Column(TypeName = "decimal(18,2)")]
        public decimal Balance { get; set; } = 0.00m;

        [Required]
        [MaxLength(20)]
        public string AccountType { get; set; } = "Checking";

        public bool IsActive { get; set; } = true;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

        // Navigation properties
        [ForeignKey("BusinessId")]
        public virtual Business? Business { get; set; }
        
        public virtual ICollection<Student> Students { get; set; } = new List<Student>();
        
        public virtual ICollection<Transaction> FromTransactions { get; set; } = new List<Transaction>();
        
        public virtual ICollection<Transaction> ToTransactions { get; set; } = new List<Transaction>();
    }
}
