from prometheus_client import make_wsgi_app
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from wsgiref.simple_server import make_server
import requests
import settings
import sys


def get_sensor_data(host):
    result = []
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    r = requests.get(
        '{}/properties?token={}'.format(host, settings.WOT_TOKEN),
        verify=settings.WOT_VERIFY_SSL,
        headers=headers
    )

    # Raise for error
    r.raise_for_status()

    for i in r.json():
        if i.get('values', False):
            result.append(i)
    return result


class WOTCollector(object):
    def collect(self):

        if not settings.WOT_ENDPOINTS:
            print('No endpoints found. Exiting.')
            sys.exit(1)

        for device in settings.WOT_ENDPOINTS.split(','):
            sensor_data = get_sensor_data(device)
            for data in sensor_data:
                c = GaugeMetricFamily(
                    data['id'],
                    data['name'],
                )

                k = list(data['values'].keys())

                # We don't care about the timestamp
                k.remove('timestamp')

                for v in k:
                        c.add_metric(v, data['values'][v])
                yield c


def main():
    REGISTRY.register(WOTCollector())
    app = make_wsgi_app()
    httpd = make_server('', 8000, app)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
