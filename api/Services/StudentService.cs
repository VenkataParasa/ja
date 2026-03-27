using Microsoft.EntityFrameworkCore;
using JABizTown.API.Data;
using JABizTown.API.Models;

namespace JABizTown.API.Services
{
    public class StudentService : IStudentService
    {
        private readonly JABizTownDbContext _context;

        public StudentService(JABizTownDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Student>> GetAllStudentsAsync()
        {
            return await _context.Students
                .Include(s => s.Role)
                .Include(s => s.Business)
                .ToListAsync();
        }

        public async Task<Student?> GetStudentByIdAsync(int id)
        {
            return await _context.Students
                .Include(s => s.Role)
                .Include(s => s.Business)
                .FirstOrDefaultAsync(s => s.StudentId == id);
        }
    }
}
