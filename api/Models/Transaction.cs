using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace JABizTown.API.Models
{
    public class Transaction
    {
        [Key]
        public int TransactionId { get; set; }

        public int? FromAccountId { get; set; }

        public int? ToAccountId { get; set; }

        [Required]
        [Column(TypeName = "decimal(18,2)")]
        public decimal Amount { get; set; }

        [Required]
        [MaxLength(20)]
        public string TransactionType { get; set; } = string.Empty; // 'Deposit', 'Withdrawal', 'Transfer', 'Salary'

        [MaxLength(200)]
        public string? Description { get; set; }

        public DateTime TransactionDate { get; set; } = DateTime.UtcNow;

        public int? BusinessId { get; set; }

        public int? StudentId { get; set; }

        // Navigation properties
        [ForeignKey("FromAccountId")]
        public virtual BankAccount? FromAccount { get; set; }

        [ForeignKey("ToAccountId")]
        public virtual BankAccount? ToAccount { get; set; }

        [ForeignKey("BusinessId")]
        public virtual Business? Business { get; set; }

        [ForeignKey("StudentId")]
        public virtual Student? Student { get; set; }
    }
}
