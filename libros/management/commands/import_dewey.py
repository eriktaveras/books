import pandas as pd
from django.core.management.base import BaseCommand
from libros.models import DeweyCode

class Command(BaseCommand):
    help = 'Import Dewey codes from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='data/DEWEY.csv',
                            help='CSV file with Dewey codes')
        parser.add_argument('--create-missing', action='store_true',
                            help='Create missing Dewey codes based on book data')

    def handle(self, *args, **options):
        file_path = options['file']
        create_missing = options['create_missing']
        self.stdout.write(self.style.SUCCESS(f'Reading from {file_path}'))
        
        # Read the CSV file
        try:
            df = pd.read_csv(file_path)
            
            # Check if the required columns exist
            if 'class_code' not in df.columns or 'class_type' not in df.columns:
                self.stdout.write(self.style.ERROR(
                    f'CSV file must contain "class_code" and "class_type" columns. Found: {df.columns.tolist()}'
                ))
                return
            
            # Count before import
            count_before = DeweyCode.objects.count()
            
            # Import data
            codes_created = 0
            codes_updated = 0
            
            for _, row in df.iterrows():
                code = str(row['class_code']).strip()
                description = str(row['class_type']).strip()
                
                # Skip empty rows
                if not code or code == 'nan' or not description or description == 'nan':
                    continue
                
                # Try to find existing code or create new
                dewey_code, created = DeweyCode.objects.update_or_create(
                    code=code,
                    defaults={'description': description}
                )
                
                if created:
                    codes_created += 1
                else:
                    codes_updated += 1
            
            # If requested, create missing codes used in the books
            if create_missing:
                self.stdout.write(self.style.SUCCESS('Creating missing Dewey codes from book data...'))
                
                # Get unique codes from BCF.csv
                try:
                    books_df = pd.read_csv('data/BCF.csv', encoding='latin1')
                    
                    if 'code' in books_df.columns:
                        import re
                        
                        # Get existing codes for faster lookup
                        existing_codes = set(DeweyCode.objects.values_list('code', flat=True))
                        
                        missing_created = 0
                        
                        for idx, row in books_df.iterrows():
                            if pd.isna(row.get('code')):
                                continue
                                
                            full_code = str(row.get('code')).strip()
                            if not full_code or full_code == 'nan':
                                continue
                                
                            # Extract Dewey code part (e.g. 001.42 from C001.42 B139m)
                            dewey_match = re.search(r'[C]?(\d+\.\d+)', full_code)
                            if dewey_match:
                                dewey_code = dewey_match.group(1)
                                
                                # Check if we already have this code (exact match)
                                if dewey_code in existing_codes:
                                    continue
                                    
                                # Check if we have it with trailing zeros removed
                                stripped_code = dewey_code.rstrip('0').rstrip('.')
                                if stripped_code in existing_codes:
                                    continue
                                    
                                # Check if we have it as a float
                                try:
                                    float_code = str(float(dewey_code))
                                    if float_code in existing_codes:
                                        continue
                                except ValueError:
                                    pass
                                
                                # Create new code with generic description
                                description = f"Clasificación {dewey_code} (Auto-generado)"
                                DeweyCode.objects.create(code=dewey_code, description=description)
                                missing_created += 1
                                existing_codes.add(dewey_code)  # Add to our set to avoid duplicates
                        
                        self.stdout.write(self.style.SUCCESS(f'Created {missing_created} missing Dewey codes from book data'))
                        codes_created += missing_created
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating missing codes: {str(e)}'))
            
            # Count after import
            count_after = DeweyCode.objects.count()
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported Dewey codes. Created: {codes_created}, Updated: {codes_updated}, '
                f'Total: {count_after} (Before: {count_before})'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing Dewey codes: {str(e)}')) 