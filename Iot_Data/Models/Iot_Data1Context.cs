using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace Iot_Data.Models
{
    public partial class Iot_Data1Context : DbContext
    {
        public Iot_Data1Context()
        {
        }

        public Iot_Data1Context(DbContextOptions<Iot_Data1Context> options)
            : base(options)
        {
        }

        public virtual DbSet<AmThanh> AmThanhs { get; set; } = null!;
        public DbSet<Prediction> Predictions { get; set; }
        public virtual DbSet<AnhSang> AnhSangs { get; set; } = null!;
        public virtual DbSet<DoAm> DoAms { get; set; } = null!;
        public virtual DbSet<Ga> Gas { get; set; } = null!;
        public virtual DbSet<NhietDo> NhietDos { get; set; } = null!;

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer("Server=DESKTOP-FF9VATI;Database=Iot_Data1;integrated security=true;");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<AmThanh>(entity =>
            {
                entity.ToTable("AmThanh");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.GiaTri)
                    .HasColumnType("decimal(8, 2)")
                    .HasColumnName("giaTri");

                entity.Property(e => e.Nhan)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("nhan");

                entity.Property(e => e.ThoiGian)

                    .HasColumnName("thoiGian");
            });

            modelBuilder.Entity<AnhSang>(entity =>
            {
                entity.ToTable("AnhSang");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.GiaTri)
                    .HasColumnType("decimal(8, 2)")
                    .HasColumnName("giaTri");

                entity.Property(e => e.Nhan)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("nhan");

                entity.Property(e => e.ThoiGian)
                    .HasColumnName("thoiGian");
            });

            modelBuilder.Entity<DoAm>(entity =>
            {
                entity.ToTable("DoAm");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.GiaTri)
                    .HasColumnType("decimal(8, 2)")
                    .HasColumnName("giaTri");

                entity.Property(e => e.Nhan)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("nhan");

                entity.Property(e => e.ThoiGian)
                    .HasColumnName("thoiGian");
            });

            modelBuilder.Entity<Ga>(entity =>
            {
                entity.ToTable("Gas");
                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.GiaTri)
                    .HasColumnType("decimal(8, 2)")
                    .HasColumnName("giaTri");

                entity.Property(e => e.Nhan)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("nhan");

                entity.Property(e => e.ThoiGian)
                    .HasColumnName("thoiGian");
            });

            modelBuilder.Entity<NhietDo>(entity =>
            {
                entity.ToTable("NhietDo");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.GiaTri)
                    .HasColumnType("decimal(8, 2)")
                    .HasColumnName("giaTri");

                entity.Property(e => e.Nhan)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("nhan");

                entity.Property(e => e.ThoiGian)
                    .HasColumnName("thoiGian");
            });
            modelBuilder.Entity<Prediction>(entity =>
            {
                entity.ToTable("Predictions");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.Label1)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("Label1");

                entity.Property(e => e.Label2)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("Label2");
                entity.Property(e => e.Label3)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("Label3");
                entity.Property(e => e.Label4)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("Label4");
                entity.Property(e => e.Label5)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("Label5");

                entity.Property(e => e.Timestamp)
                    .HasColumnName("Timestamp");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
