using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace IntellMedREST.Migrations
{
    public partial class t2 : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "Name",
                table: "Cases",
                newName: "Sex");

            migrationBuilder.AddColumn<DateTime>(
                name: "BirthDate",
                table: "Cases",
                type: "timestamp without time zone",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<string>(
                name: "FirstName",
                table: "Cases",
                type: "text",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "LastName",
                table: "Cases",
                type: "text",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Patron",
                table: "Cases",
                type: "text",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "BirthDate",
                table: "Cases");

            migrationBuilder.DropColumn(
                name: "FirstName",
                table: "Cases");

            migrationBuilder.DropColumn(
                name: "LastName",
                table: "Cases");

            migrationBuilder.DropColumn(
                name: "Patron",
                table: "Cases");

            migrationBuilder.RenameColumn(
                name: "Sex",
                table: "Cases",
                newName: "Name");
        }
    }
}
