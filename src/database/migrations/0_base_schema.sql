CREATE TABLE IF NOT EXISTS certs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain  TEXT not null,
                cert_path TEXT not null,
                key_path TEXT not null,
                ca_path TEXT null
            );

            CREATE TABLE requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method TEXT not null,
                domain TEXT not null,
                path TEXT not null,
                path_without_params not null,
                protocol TEXT not null CHECK( protocol IN ('http','https')),
                request_type TEXT,
                request_mime TEXT,
                response_mime TEXT,
                response_mime_tetected TEXT,
                raw_request_body_file TEXT,
                parsed_request_body_file TEXT,
                request_timestamp_unix_nanosecond INTEGER,
                response_timestamp_unix_nanosecond INTEGER, 
                response_status_code INTEGER CHECK( response_status_code IN ('100,101,102,103,200,201,202,203,204,205,206,207,208,209,300,301,302,303,304,305,306,307,308,305,306,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,421,422,423,424,425,426,427,428,429,431,451,500,501,502,503,504,505,506,507,508,510,511') )
            );

            CREATE TABLE IF NOT EXISTS http_headers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT not null,
                value TEXT not null,
                request_id INTEGER,
                is_response INTEGER CHECK(is_response IN (0,1)) DEFAULT 0,
                FOREIGN KEY(request_id) REFERENCES requests(id)
            );

            CREATE TABLE IF NOT EXISTS request_http_params (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER,
                param_location TEXT CHECK(param_location IN ('BODY','URL')),
                name TEXT,
                value TEXT,
                value_in_file INTEGER not null CHECK(value_in_file IN (0,1)) DEFAULT 0,
                value_is_array INTEGER not null CHECK(value_is_array IN (0,1)) DEFAULT 0,
                saved_sucessfully INTEGER CHECK((value_in_file == 0 and saved_sucessfully == null) or (value_in_file == 1 and saved_sucessfully IN (0,1))),
                value_index INTEGER,
                FOREIGN KEY(request_id) REFERENCES requests(id)
            );

            CREATE INDEX idx_request_http_params ON request_http_params (name);
            CREATE INDEX idx_request_http_params_array ON request_http_params (id,request_id,param_location,name,value_is_array,value_index);

            CREATE TABLE IF NOT EXISTS http_cookies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER,
                name TEXT not null,
                value TEXT,
                expiration_timestamp TEXT,
                max_age INT,
                http_only  INTEGER CHECK(http_only IN (0,1)),
                secure INTEGER CHECK(http_only IN (0,1)),
                same_site_policy TEXT CHECK(same_site_policy IN ('Strict','Lax','None')),
                is_response INTEGER CHECK(is_response IN (0,1)) DEFAULT 0,
                
                FOREIGN KEY(request_id) REFERENCES requests(id)
            );

            CREATE table IF NOT EXISTS redirect (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_from TEXT not null,
                url_to TEXT not null,
                method TEXT not null,
                http_status_code INTEGER not null CHECK( http_status_code IN (301,302,303,304,305,306,307,308) ) DEFAULT 301,
                use_in_https  INTEGER not null CHECK(use_in_https IN (0,1)) DEFAULT 0,
                use_in_http  INTEGER not null CHECK(use_in_http IN (0,1)) DEFAULT 1,
                exact_match INTEGER not null CHECK(exact_match IN (0,1)) DEFAULT 1,
                UNIQUE(url_from,method,http_status_code,use_in_http,exact_match),
                UNIQUE(url_from,method,http_status_code,use_in_https,exact_match)
                CHECK(use_in_http=1 or use_in_https=1)
            );
            
            DROP TRIGGER IF EXISTS remove_http_https;
            CREATE TRIGGER remove_http_https AFTER INSERT ON redirect
            BEGIN
                UPDATE redirect 
                SET url_from = REPLACE(REPLACE(NEW.url_from,'http://',''),'https://','') 
                WHERE rowid=NEW.rowid;
            END;

            DROP TRIGGER IF EXISTS remove_http_https_update;
            CREATE TRIGGER remove_http_https_update AFTER UPDATE ON redirect
            BEGIN
                UPDATE redirect 
                SET url_from = REPLACE(REPLACE(NEW.url_from,'http://',''),'https://','') 
                WHERE rowid=NEW.rowid;
            END;
