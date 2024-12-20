# src/dns_resolver.py
import dns.resolver
import socket
from typing import Dict, List, Any

class DNSResolver:
    @staticmethod
    def resolve_domain(domain: str) -> Dict[str, Any]:
        """
        Comprehensive DNS Resolution with Detailed Mapping
        """
        resolution_steps = []
        resolution_mapping = {
            'domain': domain,
            'resolution_path': []
        }

        try:
            # Step 1: Local DNS Cache Check
            resolution_steps.append("Initiating DNS Resolution")
            resolution_mapping['resolution_path'].append({
                'stage': 'Local DNS Cache',
                'description': 'Checking local system DNS cache',
                'status': 'Checked'
            })

            # Step 2: Resolve through DNS Resolver
            resolution_steps.append("Querying DNS Servers")
            
            # Root DNS Server Simulation
            resolution_mapping['resolution_path'].append({
                'stage': 'Root DNS Server',
                'description': 'Querying root nameservers',
                'status': 'Queried'
            })

            # Actual DNS Resolution
            answers = dns.resolver.resolve(domain, 'A')
            ip_address = str(answers[0])

            # TLD Server Simulation
            resolution_mapping['resolution_path'].append({
                'stage': 'Top-Level Domain (TLD) Server',
                'description': 'Obtaining domain namespace information',
                'status': 'Resolved'
            })

            # Authoritative Name Server Simulation
            resolution_mapping['resolution_path'].append({
                'stage': 'Authoritative Name Server',
                'description': 'Retrieving specific IP address',
                'ip_address': ip_address,
                'status': 'Completed'
            })

            # Final Mapping Details
            resolution_mapping.update({
                'ip_address': ip_address,
                'record_type': 'A',
                'ttl': answers.ttl
            })

            resolution_steps.append(f"Successfully resolved {domain} to {ip_address}")

            return {
                'resolution_steps': resolution_steps,
                'resolution_mapping': resolution_mapping
            }

        except dns.resolver.NXDOMAIN:
            resolution_mapping['error'] = 'Domain does not exist'
            resolution_steps.append("Error: Domain does not exist")
            
        except dns.resolver.NoAnswer:
            resolution_mapping['error'] = 'No DNS records found'
            resolution_steps.append("Error: No DNS records found")
        
        except Exception as e:
            resolution_mapping['error'] = str(e)
            resolution_steps.append(f"Unexpected error: {str(e)}")

        return {
            'resolution_steps': resolution_steps,
            'resolution_mapping': resolution_mapping
        }
