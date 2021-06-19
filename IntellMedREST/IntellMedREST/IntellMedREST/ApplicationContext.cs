using IntellMedREST.Data;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace IntellMedREST
{
	public class ApplicationContext : DbContext
	{
		//public DbSet<Case> Cases { get; set; }
		public DbSet<Case> Cases { get; set; }
			
		public DbSet<Diag> Diags { get; set; }
		//public DbSet<Lech> Lechs { get; set; }
		//public DbSet<Lek> Leks { get; set; }


		protected override void OnModelCreating(ModelBuilder modelBuilder)
		{

			modelBuilder.Entity<Diag>()
			  .HasKey(t=>t.ID);
			modelBuilder.Entity<Lech>()
			  .HasKey(t => t.ID);
			modelBuilder.Entity<Lek>()
			  .HasKey(t => t.ID);

			modelBuilder.Entity<Case>()
			  .HasMany(c => c.Diags)
			  .WithOne(e => e.Case);


		}
	

	public ApplicationContext()
		{
			//Database.EnsureCreated();
		}
		protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
		{
			optionsBuilder.UseNpgsql("Host=localhost;Port=5432;Database=med_expert;Username=postgres;Password=123");
		}
	}
}
