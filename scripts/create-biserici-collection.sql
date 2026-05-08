-- Creează colecția ec_biserici pentru directorul de biserici
BEGIN;

-- 1. Colecția în EmDash
INSERT INTO _emdash_collections (id, slug, label, description, created_at, updated_at)
VALUES (
  '01KRTQ00000000000000000C01',
  'biserici',
  'Biserici',
  'Director de biserici ortodoxe din România',
  NOW(),
  NOW()
) ON CONFLICT (slug) DO NOTHING;

-- 2. Tabelul de date
CREATE TABLE IF NOT EXISTS ec_biserici (
  id TEXT PRIMARY KEY,
  slug TEXT UNIQUE,
  status TEXT DEFAULT 'draft',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  published_at TEXT,
  locale TEXT NOT NULL DEFAULT 'ro',
  -- Custom fields
  name TEXT NOT NULL DEFAULT '',
  county TEXT DEFAULT '',
  county_slug TEXT DEFAULT '',
  city TEXT DEFAULT '',
  address TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  email TEXT DEFAULT '',
  website TEXT DEFAULT '',
  priest_name TEXT DEFAULT '',
  schedule TEXT DEFAULT '',
  google_maps_url TEXT DEFAULT '',
  lat TEXT DEFAULT '',
  lng TEXT DEFAULT '',
  patron_saint_slug TEXT DEFAULT '',
  patron_feast_date TEXT DEFAULT '',
  photo_url TEXT DEFAULT '',
  description JSON DEFAULT 'null'
);

-- 3. Câmpuri în _emdash_fields
INSERT INTO _emdash_fields (id, collection_id, slug, label, type, column_type, required, "unique", sort_order, searchable, translatable)
VALUES
  ('01KRTQ00000000000BC001', '01KRTQ00000000000000000C01', 'name',               'Nume biserică',       'string',       'text',    true,  false, 1,  true,  false),
  ('01KRTQ00000000000BC002', '01KRTQ00000000000000000C01', 'county',             'Județ',               'string',       'text',    false, false, 2,  true,  false),
  ('01KRTQ00000000000BC003', '01KRTQ00000000000000000C01', 'county_slug',        'Slug județ',          'string',       'text',    false, false, 3,  false, false),
  ('01KRTQ00000000000BC004', '01KRTQ00000000000000000C01', 'city',               'Localitate',          'string',       'text',    false, false, 4,  true,  false),
  ('01KRTQ00000000000BC005', '01KRTQ00000000000000000C01', 'address',            'Adresă',              'string',       'text',    false, false, 5,  false, false),
  ('01KRTQ00000000000BC006', '01KRTQ00000000000000000C01', 'phone',              'Telefon',             'string',       'text',    false, false, 6,  false, false),
  ('01KRTQ00000000000BC007', '01KRTQ00000000000000000C01', 'email',              'Email',               'string',       'text',    false, false, 7,  false, false),
  ('01KRTQ00000000000BC008', '01KRTQ00000000000000000C01', 'website',            'Website',             'string',       'text',    false, false, 8,  false, false),
  ('01KRTQ00000000000BC009', '01KRTQ00000000000000000C01', 'priest_name',        'Preot paroh',         'string',       'text',    false, false, 9,  true,  false),
  ('01KRTQ00000000000BC010', '01KRTQ00000000000000000C01', 'schedule',           'Program liturghii',   'string',       'text',    false, false, 10, false, false),
  ('01KRTQ00000000000BC011', '01KRTQ00000000000000000C01', 'google_maps_url',    'Google Maps URL',     'string',       'text',    false, false, 11, false, false),
  ('01KRTQ00000000000BC012', '01KRTQ00000000000000000C01', 'lat',                'Latitudine',          'string',       'text',    false, false, 12, false, false),
  ('01KRTQ00000000000BC013', '01KRTQ00000000000000000C01', 'lng',                'Longitudine',         'string',       'text',    false, false, 13, false, false),
  ('01KRTQ00000000000BC014', '01KRTQ00000000000000000C01', 'patron_saint_slug',  'Sfânt patron (slug)', 'string',       'text',    false, false, 14, false, false),
  ('01KRTQ00000000000BC015', '01KRTQ00000000000000000C01', 'patron_feast_date',  'Hramul (data)',       'string',       'text',    false, false, 15, false, false),
  ('01KRTQ00000000000BC016', '01KRTQ00000000000000000C01', 'photo_url',          'Foto principală URL', 'string',       'text',    false, false, 16, false, false),
  ('01KRTQ00000000000BC017', '01KRTQ00000000000000000C01', 'description',        'Descriere',           'portableText', 'json',    false, false, 17, false, false)
ON CONFLICT (id) DO NOTHING;

COMMIT;
