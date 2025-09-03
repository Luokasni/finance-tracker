-- Drop old tables if they exist
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS user;

-- Create user table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    monthly_income DECIMAL(10,2) NOT NULL,
    savings_goal DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2) NOT NULL,
    trans_type ENUM('income', 'expense') NOT NULL,
    category VARCHAR(50),
    trans_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Stored procedure to check savings goal
DELIMITER //
CREATE PROCEDURE CheckSavingsGoal(IN uid INT)
BEGIN
    DECLARE total_savings DECIMAL(10,2);

    SELECT SUM(CASE WHEN trans_type = 'income' THEN amount ELSE -amount END)
    INTO total_savings
    FROM transactions
    WHERE user_id = uid;

    IF total_savings IS NULL THEN
        SET total_savings = 0;
    END IF;

    SELECT u.name, u.savings_goal, total_savings,
           CASE 
             WHEN total_savings >= u.savings_goal THEN 'Goal Achieved 🎉'
             ELSE 'Keep Saving 💰'
           END AS status
    FROM user u
    WHERE u.id = uid;
END //
DELIMITER ;
