using System;
using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

namespace IntellMedREST.Migrations
{
    public partial class t4 : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Diags_Persons_PersonID",
                table: "Diags");

            migrationBuilder.DropForeignKey(
                name: "FK_Lech_Persons_PersonID",
                table: "Lech");

            migrationBuilder.DropForeignKey(
                name: "FK_Lek_Persons_PersonID",
                table: "Lek");

            migrationBuilder.DropTable(
                name: "Persons");

            migrationBuilder.RenameColumn(
                name: "PersonID",
                table: "Lek",
                newName: "CaseID");

            migrationBuilder.RenameIndex(
                name: "IX_Lek_PersonID",
                table: "Lek",
                newName: "IX_Lek_CaseID");

            migrationBuilder.RenameColumn(
                name: "PersonID",
                table: "Lech",
                newName: "CaseID");

            migrationBuilder.RenameIndex(
                name: "IX_Lech_PersonID",
                table: "Lech",
                newName: "IX_Lech_CaseID");

            migrationBuilder.RenameColumn(
                name: "PersonID",
                table: "Diags",
                newName: "CaseID");

            migrationBuilder.RenameIndex(
                name: "IX_Diags_PersonID",
                table: "Diags",
                newName: "IX_Diags_CaseID");

            migrationBuilder.CreateTable(
                name: "Cases",
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
                    table.PrimaryKey("PK_Cases", x => x.ID);
                });

            migrationBuilder.AddForeignKey(
                name: "FK_Diags_Cases_CaseID",
                table: "Diags",
                column: "CaseID",
                principalTable: "Cases",
                principalColumn: "ID",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_Lech_Cases_CaseID",
                table: "Lech",
                column: "CaseID",
                principalTable: "Cases",
                principalColumn: "ID",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_Lek_Cases_CaseID",
                table: "Lek",
                column: "CaseID",
                principalTable: "Cases",
                principalColumn: "ID",
                onDelete: ReferentialAction.Restrict);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Diags_Cases_CaseID",
                table: "Diags");

            migrationBuilder.DropForeignKey(
                name: "FK_Lech_Cases_CaseID",
                table: "Lech");

            migrationBuilder.DropForeignKey(
                name: "FK_Lek_Cases_CaseID",
                table: "Lek");

            migrationBuilder.DropTable(
                name: "Cases");

            migrationBuilder.RenameColumn(
                name: "CaseID",
                table: "Lek",
                newName: "PersonID");

            migrationBuilder.RenameIndex(
                name: "IX_Lek_CaseID",
                table: "Lek",
                newName: "IX_Lek_PersonID");

            migrationBuilder.RenameColumn(
                name: "CaseID",
                table: "Lech",
                newName: "PersonID");

            migrationBuilder.RenameIndex(
                name: "IX_Lech_CaseID",
                table: "Lech",
                newName: "IX_Lech_PersonID");

            migrationBuilder.RenameColumn(
                name: "CaseID",
                table: "Diags",
                newName: "PersonID");

            migrationBuilder.RenameIndex(
                name: "IX_Diags_CaseID",
                table: "Diags",
                newName: "IX_Diags_PersonID");

            migrationBuilder.CreateTable(
                name: "Persons",
                columns: table => new
                {
                    ID = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    DB = table.Column<DateTime>(type: "timestamp without time zone", nullable: false),
                    DS = table.Column<string>(type: "text", nullable: true),
                    Fam = table.Column<string>(type: "text", nullable: true),
                    Im = table.Column<string>(type: "text", nullable: true),
                    Ot = table.Column<string>(type: "text", nullable: true),
                    Stad = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Persons", x => x.ID);
                });

            migrationBuilder.AddForeignKey(
                name: "FK_Diags_Persons_PersonID",
                table: "Diags",
                column: "PersonID",
                principalTable: "Persons",
                principalColumn: "ID",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_Lech_Persons_PersonID",
                table: "Lech",
                column: "PersonID",
                principalTable: "Persons",
                principalColumn: "ID",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_Lek_Persons_PersonID",
                table: "Lek",
                column: "PersonID",
                principalTable: "Persons",
                principalColumn: "ID",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
