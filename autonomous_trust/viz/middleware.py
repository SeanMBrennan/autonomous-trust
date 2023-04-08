import os
from sassutils.wsgi import SassMiddleware
from sass import CompileError


class SassASGIMiddleware(SassMiddleware):
    def __init__(self, app, manifests, package_dir={}, error_status='200 OK'):
        self.logger = app.logger
        super().__init__(app.asgi_app, manifests, package_dir, error_status)

    async def __call__(self, scope, recv, send):  # noqa
        path = scope.get('path', '/')
        if path.endswith('.css'):
            for prefix, package_dir, manifest in self.paths:
                if not path.startswith(prefix):
                    continue
                css_filename = path[len(prefix):]
                sass_filename = manifest.unresolve_filename(package_dir, css_filename)
                src_dir = manifest.sass_path
                if not os.path.isabs(manifest.sass_path):
                    src_dir = os.path.join(package_dir, manifest.sass_path)
                if not os.path.exists(os.path.join(src_dir, sass_filename)):
                    continue
                tgt_dir = manifest.css_path
                if not os.path.isabs(manifest.css_path):
                    tgt_dir = os.path.join(package_dir, manifest.css_path)
                css_path = os.path.join(tgt_dir, css_filename)
                try:
                    self.logger.info('Compile %s' % os.path.join(src_dir, sass_filename))
                    manifest.build_one(os.path.dirname(src_dir), sass_filename, source_map=True)
                except (IOError, OSError) as err:
                    self.logger.error(str(err))
                    break
                except CompileError as err:
                    self.logger.error(str(err))
                    os.remove(css_path)
        return await self.app(scope, recv, send)