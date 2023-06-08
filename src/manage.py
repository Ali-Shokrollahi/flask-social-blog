from flask.cli import AppGroup

from app import create_app, mysql

app = create_app()
db_cli = AppGroup('db', help='Database commands.')


@db_cli.command('setup')
def create_tables():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute(
            '''
        CREATE TABLE IF NOT EXISTS `Users`(
            `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `email` VARCHAR(128) NOT NULL,
            `username` VARCHAR(32) NOT NULL,
            `password` VARCHAR(255) NOT NULL,
            `first_name` VARCHAR(32) NOT NULL,
            `last_name` VARCHAR(32) NOT NULL,
            `bio` VARCHAR(255) NULL,
            `date_joined` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
            `last_login` TIMESTAMP DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
            `is_active` TINYINT(1) NOT NULL DEFAULT 1,
            `image` VARCHAR(255) NULL,
            `role` ENUM('superuser','admin','writer') NOT NULL DEFAULT 'writer',
            CONSTRAINT `users_email_unique` UNIQUE (`email`),
            CONSTRAINT `users_username_unique` UNIQUE (`username`)
            );
            '''
        )

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS `Category`(
                `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(64) NOT NULL,
                `description` VARCHAR(255)  NULL,
                `creator` BIGINT UNSIGNED NOT NULL,
                CONSTRAINT `category_creator_foreign` FOREIGN KEY (`creator`) REFERENCES `Users` (`id`) ON DELETE RESTRICT
            );
            '''
        )

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS `Posts`(
                `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `title` VARCHAR(128) NOT NULL,
                `slug` VARCHAR(128) NOT NULL,
                `summary` VARCHAR(255) NULL,
                `content` TEXT NOT NULL,
                `cover` VARCHAR(255) NULL,
                `created_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                `updated_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
                `status` ENUM('published','draft','banned') NOT NULL DEFAULT 'draft',
                `owner_id` BIGINT UNSIGNED NOT NULL,
                `category_id` BIGINT UNSIGNED NOT NULL,
                CONSTRAINT `posts_slug_unique` UNIQUE (`slug`),
                CONSTRAINT `posts_owner_id_foreign` FOREIGN KEY (`owner_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE,
                CONSTRAINT `posts_category_id_foreign` FOREIGN KEY (`category_id`) REFERENCES `Category` (`id`) ON DELETE RESTRICT
            );
            '''
        )

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS `Contacts`(
                `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `email` VARCHAR(128) NOT NULL,
                `full_name` VARCHAR(64) NOT NULL,
                `subject` VARCHAR(128) NOT NULL,
                `message` TEXT NOT NULL,
                `created_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                `status` ENUM('unread','read') NOT NULL DEFAULT 'unread'
            );
            '''
        )

        cur.close()
        mysql.connection.commit()

    print('Tables created successfully.')


app.cli.add_command(db_cli)

if __name__ == '__main__':
    app.cli()
