-- FleetFlow Complete Schema
-- Run this in pgAdmin or psql BEFORE starting the backend

-- Create the database first (run separately if needed):
-- CREATE DATABASE fleetflow;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TYPE vehicle_status_enum AS ENUM ('available','on_trip','in_shop','retired');
CREATE TYPE driver_status_enum AS ENUM ('available','on_trip','off_duty','suspended');
CREATE TYPE trip_status_enum AS ENUM ('draft','dispatched','completed','cancelled');
CREATE TYPE vehicle_type_enum AS ENUM ('truck','van','bike','car');
CREATE TYPE expense_category_enum AS ENUM ('fuel','maintenance','toll','fine','insurance','other');

CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(50) NOT NULL UNIQUE, description TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
INSERT INTO roles (name, description) VALUES
  ('fleet_manager','Fleet Manager'), ('dispatcher','Dispatcher'),
  ('safety_officer','Safety Officer'), ('financial_analyst','Financial Analyst');

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE, password_hash TEXT NOT NULL,
  full_name VARCHAR(200) NOT NULL, is_active BOOLEAN NOT NULL DEFAULT TRUE,
  last_login_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE user_roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, role_id)
);

CREATE TABLE vehicles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL, license_plate VARCHAR(20) NOT NULL UNIQUE,
  vehicle_type vehicle_type_enum NOT NULL,
  make VARCHAR(100), model VARCHAR(100), year SMALLINT CHECK (year>=1990 AND year<=2100),
  max_capacity_kg NUMERIC(10,2) NOT NULL CHECK (max_capacity_kg>0),
  odometer_km NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (odometer_km>=0),
  status vehicle_status_enum NOT NULL DEFAULT 'available',
  acquisition_cost NUMERIC(12,2), acquired_at DATE, region VARCHAR(100), notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE vehicle_status_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
  old_status vehicle_status_enum, new_status vehicle_status_enum NOT NULL,
  reason TEXT, changed_by UUID REFERENCES users(id),
  changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE drivers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  full_name VARCHAR(200) NOT NULL, employee_id VARCHAR(50) UNIQUE,
  phone VARCHAR(20), email VARCHAR(255) UNIQUE,
  license_number VARCHAR(50) NOT NULL UNIQUE, license_category VARCHAR(20) NOT NULL,
  license_expiry_date DATE NOT NULL,
  safety_score NUMERIC(4,2) DEFAULT 100 CHECK (safety_score>=0 AND safety_score<=100),
  status driver_status_enum NOT NULL DEFAULT 'available',
  trips_completed INTEGER NOT NULL DEFAULT 0, trips_total INTEGER NOT NULL DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE driver_status_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
  old_status driver_status_enum, new_status driver_status_enum NOT NULL,
  reason TEXT, changed_by UUID REFERENCES users(id),
  changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE trips (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID NOT NULL REFERENCES vehicles(id),
  driver_id UUID NOT NULL REFERENCES drivers(id),
  created_by UUID REFERENCES users(id),
  origin VARCHAR(300) NOT NULL, destination VARCHAR(300) NOT NULL,
  cargo_description TEXT, cargo_weight_kg NUMERIC(10,2) NOT NULL CHECK (cargo_weight_kg>=0),
  status trip_status_enum NOT NULL DEFAULT 'draft',
  scheduled_at TIMESTAMPTZ, dispatched_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ, cancelled_at TIMESTAMPTZ, cancel_reason TEXT,
  odometer_start NUMERIC(12,2), odometer_end NUMERIC(12,2),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE trip_status_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trip_id UUID NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
  old_status trip_status_enum, new_status trip_status_enum NOT NULL,
  notes TEXT, changed_by UUID REFERENCES users(id),
  changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE maintenance_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID NOT NULL REFERENCES vehicles(id),
  performed_by UUID REFERENCES users(id),
  service_type VARCHAR(200) NOT NULL, description TEXT,
  cost NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (cost>=0),
  start_date DATE NOT NULL, end_date DATE, vendor_name VARCHAR(200),
  odometer_at_service NUMERIC(12,2), is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE fuel_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID NOT NULL REFERENCES vehicles(id),
  trip_id UUID REFERENCES trips(id), logged_by UUID REFERENCES users(id),
  liters NUMERIC(8,3) NOT NULL CHECK (liters>0),
  cost_per_liter NUMERIC(8,4) NOT NULL CHECK (cost_per_liter>0),
  odometer_at_fill NUMERIC(12,2),
  fuel_date DATE NOT NULL DEFAULT CURRENT_DATE, station_name VARCHAR(200), notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE expenses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID REFERENCES vehicles(id), trip_id UUID REFERENCES trips(id),
  logged_by UUID REFERENCES users(id),
  category expense_category_enum NOT NULL,
  amount NUMERIC(12,2) NOT NULL CHECK (amount>=0),
  description TEXT, expense_date DATE NOT NULL DEFAULT CURRENT_DATE, receipt_ref VARCHAR(200),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_drivers_expiry ON drivers(license_expiry_date);
CREATE INDEX idx_trips_vehicle ON trips(vehicle_id);
CREATE INDEX idx_trips_driver ON trips(driver_id);
CREATE INDEX idx_trips_status ON trips(status);
CREATE INDEX idx_maintenance_vehicle ON maintenance_logs(vehicle_id);
CREATE INDEX idx_fuel_vehicle ON fuel_logs(vehicle_id);
CREATE INDEX idx_expenses_vehicle ON expenses(vehicle_id);

-- Auto updated_at trigger
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$ BEGIN NEW.updated_at=NOW(); RETURN NEW; END; $$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at_users BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_vehicles BEFORE UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_drivers BEFORE UPDATE ON drivers FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_trips BEFORE UPDATE ON trips FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_maintenance BEFORE UPDATE ON maintenance_logs FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_fuel BEFORE UPDATE ON fuel_logs FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_expenses BEFORE UPDATE ON expenses FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- Business logic triggers
CREATE OR REPLACE FUNCTION sync_status_on_trip()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status='dispatched' AND (OLD.status IS NULL OR OLD.status!='dispatched') THEN
    UPDATE vehicles SET status='on_trip' WHERE id=NEW.vehicle_id;
    UPDATE drivers SET status='on_trip' WHERE id=NEW.driver_id;
  ELSIF NEW.status IN ('completed','cancelled') AND OLD.status='dispatched' THEN
    UPDATE vehicles SET status='available' WHERE id=NEW.vehicle_id;
    UPDATE drivers SET status='available' WHERE id=NEW.driver_id;
  END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_status AFTER INSERT OR UPDATE OF status ON trips
  FOR EACH ROW EXECUTE FUNCTION sync_status_on_trip();

CREATE OR REPLACE FUNCTION sync_vehicle_on_maintenance()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP='INSERT' AND NEW.is_active=TRUE THEN
    UPDATE vehicles SET status='in_shop' WHERE id=NEW.vehicle_id;
  ELSIF TG_OP='UPDATE' AND NEW.is_active=FALSE AND OLD.is_active=TRUE THEN
    UPDATE vehicles SET status='available' WHERE id=NEW.vehicle_id;
  END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_maintenance AFTER INSERT OR UPDATE OF is_active ON maintenance_logs
  FOR EACH ROW EXECUTE FUNCTION sync_vehicle_on_maintenance();
