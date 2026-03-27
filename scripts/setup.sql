-- JA BizTown Database Setup Script
-- This script creates the Economic Engine database schema

-- Create the main database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'JABizTown')
BEGIN
    CREATE DATABASE JABizTown;
END
GO

USE JABizTown;
GO

-- Create Businesses table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Businesses' AND xtype='U')
BEGIN
    CREATE TABLE Businesses (
        BusinessId INT IDENTITY(1,1) PRIMARY KEY,
        BusinessName NVARCHAR(100) NOT NULL,
        BusinessType NVARCHAR(50) NOT NULL,
        Description NVARCHAR(500),
        InitialCapital DECIMAL(18,2) NOT NULL DEFAULT 5000.00,
        CurrentBalance DECIMAL(18,2) NOT NULL DEFAULT 5000.00,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        UpdatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE()
    );
END
GO

-- Create BankAccounts table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BankAccounts' AND xtype='U')
BEGIN
    CREATE TABLE BankAccounts (
        AccountId INT IDENTITY(1,1) PRIMARY KEY,
        AccountNumber NVARCHAR(20) UNIQUE NOT NULL,
        AccountHolderName NVARCHAR(100) NOT NULL,
        BusinessId INT NULL,
        Balance DECIMAL(18,2) NOT NULL DEFAULT 0.00,
        AccountType NVARCHAR(20) NOT NULL DEFAULT 'Checking',
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        UpdatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        FOREIGN KEY (BusinessId) REFERENCES Businesses(BusinessId)
    );
END
GO

-- Create Roles table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Roles' AND xtype='U')
BEGIN
    CREATE TABLE Roles (
        RoleId INT IDENTITY(1,1) PRIMARY KEY,
        RoleName NVARCHAR(50) NOT NULL,
        RoleDescription NVARCHAR(200),
        BaseSalary DECIMAL(18,2) NOT NULL DEFAULT 0.00,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE()
    );
END
GO

-- Create Students table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Students' AND xtype='U')
BEGIN
    CREATE TABLE Students (
        StudentId INT IDENTITY(1,1) PRIMARY KEY,
        FirstName NVARCHAR(50) NOT NULL,
        LastName NVARCHAR(50) NOT NULL,
        Email NVARCHAR(100),
        StudentNumber NVARCHAR(20) UNIQUE,
        BusinessId INT NULL,
        RoleId INT NULL,
        BankAccountId INT NULL,
        IsActive BIT NOT NULL DEFAULT 1,
        CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        FOREIGN KEY (BusinessId) REFERENCES Businesses(BusinessId),
        FOREIGN KEY (RoleId) REFERENCES Roles(RoleId),
        FOREIGN KEY (BankAccountId) REFERENCES BankAccounts(AccountId)
    );
END
GO

-- Create Transactions table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Transactions' AND xtype='U')
BEGIN
    CREATE TABLE Transactions (
        TransactionId INT IDENTITY(1,1) PRIMARY KEY,
        FromAccountId INT NULL,
        ToAccountId INT NULL,
        Amount DECIMAL(18,2) NOT NULL,
        TransactionType NVARCHAR(20) NOT NULL, -- 'Deposit', 'Withdrawal', 'Transfer', 'Salary'
        Description NVARCHAR(200),
        TransactionDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
        BusinessId INT NULL,
        StudentId INT NULL,
        FOREIGN KEY (FromAccountId) REFERENCES BankAccounts(AccountId),
        FOREIGN KEY (ToAccountId) REFERENCES BankAccounts(AccountId),
        FOREIGN KEY (BusinessId) REFERENCES Businesses(BusinessId),
        FOREIGN KEY (StudentId) REFERENCES Students(StudentId)
    );
END
GO

-- Insert initial JA BizTown businesses
IF NOT EXISTS (SELECT * FROM Businesses)
BEGIN
    INSERT INTO Businesses (BusinessName, BusinessType, Description, InitialCapital, CurrentBalance) VALUES
    ('City Bank', 'Financial', 'Provides banking services and manages accounts', 10000.00, 10000.00),
    ('Tech Solutions', 'Technology', 'Software development and IT services', 8000.00, 8000.00),
    ('Healthy Foods Market', 'Retail', 'Grocery store and food products', 6000.00, 6000.00),
    ('Construction Co', 'Construction', 'Building and construction services', 7500.00, 7500.00),
    ('Energy Plus', 'Utilities', 'Electric and utility services', 9000.00, 9000.00),
    ('Media Hub', 'Media', 'Advertising and media production', 5500.00, 5500.00),
    ('Healthcare Center', 'Healthcare', 'Medical and health services', 8500.00, 8500.00),
    ('Education Academy', 'Education', 'Training and educational services', 7000.00, 7000.00);
END
GO

-- Insert initial roles
IF NOT EXISTS (SELECT * FROM Roles)
BEGIN
    INSERT INTO Roles (RoleName, RoleDescription, BaseSalary) VALUES
    ('CEO', 'Chief Executive Officer', 500.00),
    ('Manager', 'Department Manager', 350.00),
    ('Accountant', 'Financial Accountant', 300.00),
    ('Developer', 'Software Developer', 280.00),
    ('Cashier', 'Bank Cashier', 200.00),
    ('Sales Associate', 'Sales Representative', 220.00),
    ('Engineer', 'Technical Engineer', 320.00),
    ('Marketing Specialist', 'Marketing Coordinator', 250.00),
    ('Doctor', 'Medical Doctor', 450.00),
    ('Teacher', 'Education Instructor', 275.00);
END
GO

-- Create bank accounts for each business
IF NOT EXISTS (SELECT * FROM BankAccounts WHERE BusinessId IS NOT NULL)
BEGIN
    INSERT INTO BankAccounts (AccountNumber, AccountHolderName, BusinessId, Balance, AccountType) 
    SELECT 
        'BIZ' + RIGHT('000' + CAST(BusinessId AS VARCHAR(3)), 3),
        BusinessName,
        BusinessId,
        CurrentBalance,
        'Business'
    FROM Businesses;
END
GO

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS IX_Transactions_TransactionDate ON Transactions(TransactionDate);
CREATE INDEX IF NOT EXISTS IX_Transactions_BusinessId ON Transactions(BusinessId);
CREATE INDEX IF NOT EXISTS IX_Students_BusinessId ON Students(BusinessId);
CREATE INDEX IF NOT EXISTS IX_BankAccounts_BusinessId ON BankAccounts(BusinessId);
GO

PRINT 'JA BizTown database setup completed successfully!';
