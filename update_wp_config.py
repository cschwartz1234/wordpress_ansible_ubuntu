import requests

def escape_php_characters(s):
    # Escapes PHP-sensitive characters in the string
    return s.replace("$", "\\$")

def insert_db_constants(db_settings):
    # Prepare the PHP code for wp-config.php with the database settings
    db_code = "\n".join([f"define('{key}', '{value}');" for key, value in db_settings.items()])
    return db_code

def update_wp_config(sample_file_path, output_file_path, db_settings):
    # Read the wp-config-sample.php file
    with open(sample_file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    added_db_settings = False
    for line in lines:
        if "database_name_here" in line:
            new_lines.append(f"define('DB_NAME', '{db_settings['DB_NAME']}');\n")
            continue
        if "username_here" in line:
            new_lines.append(f"define('DB_USER', '{db_settings['DB_USER']}');\n")
            continue
        if "password_here" in line:
            new_lines.append(f"define('DB_PASSWORD', '{db_settings['DB_PASSWORD']}');\n")
            continue
        if "localhost" in line:
            new_lines.append(f"define('DB_HOST', '{db_settings['DB_HOST']}');\n")
            continue

        # Enable WordPress debug mode and specify log file
        if "define( 'WP_DEBUG', false );" in line:
            debug_config = "\n".join([
                "define( 'WP_DEBUG', true );",
                "define( 'WP_DEBUG_LOG', '/var/www/html/wordpress/wp-content/debug.log' );",
                "define( 'WP_DEBUG_DISPLAY', false );",
                "@ini_set( 'display_errors', 0 );"
            ])
            new_lines.append(debug_config + "\n")
            continue

        new_lines.append(line)

    # Write the updated content to wp-config.php
    with open(output_file_path, 'w') as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    wp_config_sample_path = '/var/www/html/wordpress/wp-config-sample.php'
    wp_config_output_path = '/var/www/html/wordpress/wp-config.php'
    db_settings = {
        'DB_NAME': 'wordpress_db',
        'DB_USER': 'wpuser',
        'DB_PASSWORD': 'XXXXX',
        'DB_HOST': 'ansdb1',  # Use the actual IP address if necessary
    }

    update_wp_config(wp_config_sample_path, wp_config_output_path, db_settings)

