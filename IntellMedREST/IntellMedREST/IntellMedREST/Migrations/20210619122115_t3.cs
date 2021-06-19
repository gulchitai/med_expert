using System;
using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

namespace IntellMedREST.Migrations
{
    public partial class t3 : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Cases");

            migrationBuilder.CreateTable(
                name: "Persons",
                columns: table => new
                {
                    ID = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    Fam = table.Column<string>(type: "text", nullable: true),
                    Im = table.Column<string>(type: "text", nullable: true),
                    Ot = table.Column<string>(type: "text", nullable: true),
                    DB = table.Column<DateTime>(type: "timestamp without time zone", nullable: false),
                    DS = table.Column<string>(type: "text", nullable: true),
                    Stad = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Persons", x => x.ID);
                });

            migrationBuilder.CreateTable(
                name: "Diags",
                columns: table => new
                {
                    ID = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    PersonID = table.Column<int>(type: "integer", nullable: true),
                    CodeUsl = table.Column<string>(type: "text", nullable: true),
                    UslName = table.Column<string>(type: "text", nullable: true),
                    AvgQty = table.Column<decimal>(type: "numeric", nullable: false),
                    AvgMultipl = table.Column<decimal>(type: "numeric", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Diags", x => x.ID);
                    table.ForeignKey(
                        name: "FK_Diags_Persons_PersonID",
                        column: x => x.PersonID,
                        principalTable: "Persons",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "Lech",
                columns: table => new
                {
                    ID = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    PersonID = table.Column<int>(type: "integer", nullable: true),
                    CodeUsl = table.Column<string>(type: "text", nullable: true),
                    UslName = table.Column<string>(type: "text", nullable: true),
                    AvgQty = table.Column<decimal>(type: "numeric", nullable: false),
                    AvgMultipl = table.Column<decimal>(type: "numeric", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Lech", x => x.ID);
                    table.ForeignKey(
                        name: "FK_Lech_Persons_PersonID",
                        column: x => x.PersonID,
                        principalTable: "Persons",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "Lek",
                columns: table => new
                {
                    ID = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    PersonID = table.Column<int>(type: "integer", nullable: true),
                    Code = table.Column<string>(type: "text", nullable: true),
                    Class = table.Column<string>(type: "text", nullable: true),
                    Name = table.Column<string>(type: "text", nullable: true),
                    AvgQty = table.Column<decimal>(type: "numeric", nullable: false),
                    Uom = table.Column<string>(type: "text", nullable: true),
                    SSD = table.Column<int>(type: "integer", nullable: false),
                    SKD = table.Column<int>(type: "integer", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Lek", x => x.ID);
                    table.ForeignKey(
                        name: "FK_Lek_Persons_PersonID",
                        column: x => x.PersonID,
                        principalTable: "Persons",
                        principalColumn: "ID",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Diags_PersonID",
                table: "Diags",
                column: "PersonID");

            migrationBuilder.CreateIndex(
                name: "IX_Lech_PersonID",
                table: "Lech",
                column: "PersonID");

            migrationBuilder.CreateIndex(
                name: "IX_Lek_PersonID",
                table: "Lek",
                column: "PersonID");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Diags");

            migrationBuilder.DropTable(
                name: "Lech");

            migrationBuilder.DropTable(
                name: "Lek");

            migrationBuilder.DropTable(
                name: "Persons");

            migrationBuilder.CreateTable(
                name: "Cases",
                columns: table => new
                {
                    Id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    Age = table.Column<int>(type: "integer", nullable: false),
                    BirthDate = table.Column<DateTime>(type: "timestamp without time zone", nullable: false),
                    FirstName = table.Column<string>(type: "text", nullable: true),
                    LastName = table.Column<string>(type: "text", nullable: true),
                    Patron = table.Column<string>(type: "text", nullable: true),
                    Sex = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Cases", x => x.Id);
                });
        }
    }
}
