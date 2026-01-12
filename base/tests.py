import random
from faker import Faker
from faker.providers import DynamicProvider

from django.test import TestCase
from django.urls import reverse

from base.models import Lente, ObraSocial, Doctor

######################################
#### OBRAS SOCIALES TEST
######################################
class ObraSocialListViewTests(TestCase):
    def setUp(self):
        obras_sociales_provider = DynamicProvider(
            provider_name='obra_social',
            elements=['IAPOS','PAMI','OSDE','ACA SALUD','AVALIAN','ANDAR',
                      'BANCARIOS','COVER SALUD','DASUTEN','DOSUBA','ELEVAR',
                      'FEMEBA','IOMA','IOSFA','OSCHOCA','OSECAC','OSFE',
                      'OSMEDICA','OSPIC','OSPACA']
        )
        self.fake = Faker('es_AR')
        self.fake.add_provider(obras_sociales_provider)

        self.url = reverse('obra-social-list-view')

    def test_obras_social_list_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'obra_social_list.html')

    def test_lista_vacia_obra_social(self):
        """La ListView no debe devolver error cuando no existan obras sociales"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(),0)


    def test_listar_una_obra_social(self):
        """La LisView muestra la obra social cargada"""
        nombre_os = self.fake.obra_social()
        os = ObraSocial(1,nombre_os)
        os.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'],[os])

    def test_listar_varias_obras_sociales(self):
        """La ListView muestra las obras sociales cargadas"""
        obras_sociales = []
        for i in range(1,6):
            os = ObraSocial(i,self.fake.obra_social())
            os.save()
            obras_sociales.append(os)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']),obras_sociales)


class ObraSocialCreateViewTests(TestCase):
    def setUp(self):
        obras_sociales_provider = DynamicProvider(
            provider_name='obra_social',
            elements=['IAPOS','PAMI','OSDE','ACA SALUD','AVALIAN','ANDAR',
                      'BANCARIOS','COVER SALUD','DASUTEN','DOSUBA','ELEVAR',
                      'FEMEBA','IOMA','IOSFA','OSCHOCA','OSECAC','OSFE',
                      'OSMEDICA','OSPIC','OSPACA']
        )
        self.fake = Faker('es_AR')
        self.fake.add_provider(obras_sociales_provider)

        self.url = reverse('obra-social-create-view')

    def test_obras_social_create_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'obra_social_create_form.html')

    def test_crear_una_obra_social(self):
        """La CreateView crea una nueva obra social"""
        cantidad_obras_sociales_iniciales = 5
        for i in range(1,cantidad_obras_sociales_iniciales+1):
            os = ObraSocial(i,self.fake.obra_social())
            os.save()

        nombre_os = self.fake.obra_social()
        data = {
            'descripcion': nombre_os
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(ObraSocial.objects.count(),cantidad_obras_sociales_iniciales+1)
        self.assertTrue(ObraSocial.objects.filter(descripcion=nombre_os).exists())

    def test_crear_una_obra_social(self):
        """La CreateView crea la primer obra social de la base de datos"""
        nombre_os = self.fake.obra_social()
        data = {
            'descripcion': nombre_os
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(ObraSocial.objects.count(),1)
        self.assertTrue(ObraSocial.objects.filter(descripcion=nombre_os).exists())
        

class ObraSocialUpdateViewTests(TestCase):
    def setUp(self):
        obras_sociales_provider = DynamicProvider(
            provider_name='obra_social',
            elements=['IAPOS','PAMI','OSDE','ACA SALUD','AVALIAN','ANDAR',
                      'BANCARIOS','COVER SALUD','DASUTEN','DOSUBA','ELEVAR',
                      'FEMEBA','IOMA','IOSFA','OSCHOCA','OSECAC','OSFE',
                      'OSMEDICA','OSPIC','OSPACA']
        )
        self.fake = Faker('es_AR')
        self.fake.add_provider(obras_sociales_provider)

        # Creo instancias de Obra Social
        cantidad_obras_sociales_iniciales = 5
        for i in range(1,cantidad_obras_sociales_iniciales+1):
            os = ObraSocial(i,self.fake.obra_social())
            os.save()

        # Guardo la url
        self.obra_social_pk = random.randint(1, cantidad_obras_sociales_iniciales)
        self.url = reverse('obra-social-update-view',args=[self.obra_social_pk])

    def test_obra_social_update_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'obra_social_update_form.html')

    def test_modificar_nombre_obra_social(self):
        """La UpdateView debe modificar el único dato de una obra social cualquiera"""
        descripcion_new = self.fake.name()
        data = {
            'descripcion': descripcion_new
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ObraSocial.objects.filter(id=self.obra_social_pk).exists())
        self.assertEqual(ObraSocial.objects.get(id=self.obra_social_pk).descripcion, descripcion_new)

class ObraSocialDeleteViewTests(TestCase):
    def setUp(self):
        obras_sociales_provider = DynamicProvider(
            provider_name='obra_social',
            elements=['IAPOS','PAMI','OSDE','ACA SALUD','AVALIAN','ANDAR',
                      'BANCARIOS','COVER SALUD','DASUTEN','DOSUBA','ELEVAR',
                      'FEMEBA','IOMA','IOSFA','OSCHOCA','OSECAC','OSFE',
                      'OSMEDICA','OSPIC','OSPACA']
        )
        self.fake = Faker('es_AR')
        self.fake.add_provider(obras_sociales_provider)

        # Creo instancias de Obra Social
        self.cantidad_obras_sociales_iniciales = 5
        for i in range(1,self.cantidad_obras_sociales_iniciales+1):
            os = ObraSocial(i,self.fake.obra_social())
            os.save()

        # Guardo la url
        self.obra_social_pk = random.randint(1, self.cantidad_obras_sociales_iniciales)
        self.url = reverse('obra-social-delete-view',args=[self.obra_social_pk])

    def test_obra_social_confirm_delete_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'obra_social_confirm_delete.html')

    def test_borrar_obra_social(self):
        """La DeleteView debe borrar sin problemas una obra social existente"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ObraSocial.objects.count(),self.cantidad_obras_sociales_iniciales-1)
        self.assertFalse(ObraSocial.objects.filter(id=self.obra_social_pk).exists())

    def test_error_borrar_obra_social_inexistente(self):
        """La DeleteVIew debe devolver error si la obra social que se desea borrar no existe"""
        response = self.client.post(reverse('obra-social-delete-view',args=[7]))
        self.assertFalse(ObraSocial.objects.filter(id=7).exists())
        self.assertEqual(response.status_code, 404)
        
######################################
#### DOCTORES TEST
######################################
class DoctorListViewTests(TestCase):
    def setUp(self):
        self.fake = Faker('es_AR')
        self.url = reverse('doctor-list-view')

    def test_doctor_list_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'doctor_list.html')

    def test_lista_vacia_doctor(self):
        """La ListView no debe devolver error cuando no existan doctores"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(),0)


    def test_listar_un_doctor(self):
        """La LisView muestra el doctor cargado"""
        doctor = Doctor(
            id=1,
            apellido=self.fake.last_name(),
            nombre=self.fake.first_name(),
            ciudad=self.fake.city()
        )
        doctor.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'],[doctor])

    def test_listar_varios_doctores(self):
        """La ListView muestra los doctores cargadas"""
        doctores = []
        for i in range(1,6):
            doctor = Doctor(
                id=i,
                apellido=self.fake.last_name(),
                nombre=self.fake.first_name(),
                ciudad=self.fake.city()
            )
            doctor.save()
            doctores.append(doctor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']),doctores)


class DoctorCreateViewTests(TestCase):
    def setUp(self):
        self.fake = Faker('es_AR')
        self.url = reverse('doctor-create-view')

    def test_doctor_create_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'doctor_create_form.html')

    def test_crear_un_doctor(self):
        """La CreateView crea un nuevo doctor"""
        cantidad_doctores_iniciales = 5
        for i in range(1,cantidad_doctores_iniciales+1):
            doctor = Doctor(
                id=i,
                apellido=self.fake.last_name(),
                nombre=self.fake.first_name(),
                ciudad=self.fake.city()
            )
            doctor.save()

        apellido_doctor = self.fake.last_name()
        nombre_doctor = self.fake.first_name()
        data = {
            'apellido': apellido_doctor,
            'nombre': nombre_doctor,
            'ciudad': self.fake.city()
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Doctor.objects.count(),cantidad_doctores_iniciales+1)
        self.assertTrue(Doctor.objects.filter(apellido=apellido_doctor,nombre=nombre_doctor).exists())

    def test_crear_el_primer_doctor(self):
        """La CreateView crea el primer doctor de la base de datos"""
        apellido_doctor = self.fake.last_name()
        nombre_doctor = self.fake.first_name()
        data = {
            'apellido': apellido_doctor,
            'nombre': nombre_doctor,
            'ciudad': self.fake.city()
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Doctor.objects.count(),1)
        self.assertTrue(Doctor.objects.filter(apellido=apellido_doctor,nombre=nombre_doctor).exists())


class DoctorDetailViewTests(TestCase):
    def setUp(self):
        self.fake = Faker('es_AR')

        # Creo instancias de Doctor
        cantidad_doctores_iniciales = 5
        for i in range(1,cantidad_doctores_iniciales+1):
            doctor = Doctor(
                id=i,
                apellido=self.fake.last_name(),
                nombre=self.fake.first_name(),
                ciudad=self.fake.city()
            )
            doctor.save()

        # Guardo la url
        self.doctor_pk = random.randint(1, cantidad_doctores_iniciales)
        self.doctor = Doctor.objects.get(id=self.doctor_pk)
        self.url = reverse('doctor-detail-view',args=[self.doctor_pk])

    def test_doctor_detail_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'doctor_detail.html')

    def test_ver_un_doctor(self):
        """La DeleteView debe visualizar sin problemas un doctor existente"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'],self.doctor)

    def test_error_borrar_doctor_inexistente(self):
        """La DeleteVIew debe devolver error si el doctor que se desea ver no existe"""
        response = self.client.get(reverse('doctor-detail-view',args=[7]))
        self.assertFalse(Doctor.objects.filter(id=7).exists())
        self.assertEqual(response.status_code, 404)


class DoctorUpdateViewTests(TestCase):
    def setUp(self):
        self.fake = Faker('es_AR')

        # Creo instancias de Doctor
        cantidad_doctores_iniciales = 5
        for i in range(1,cantidad_doctores_iniciales+1):
            doctor = Doctor(
                id=i,
                apellido=self.fake.last_name(),
                nombre=self.fake.first_name(),
                ciudad=self.fake.city()
            )
            doctor.save()

        # Guardo la url
        self.doctor_pk = random.randint(1, cantidad_doctores_iniciales)
        self.url = reverse('doctor-update-view',args=[self.doctor_pk])

    def test_doctor_update_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'doctor_update_form.html')

    def test_modificar_apellido_doctor(self):
        """La UpdateView debe modificar el apellido de un doctor cualquiera"""
        new_data = self.fake.last_name()
        data = {
            'apellido': new_data,
            'nombre': Doctor.objects.get(id=self.doctor_pk).nombre,
            'ciudad': Doctor.objects.get(id=self.doctor_pk).ciudad
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Doctor.objects.filter(id=self.doctor_pk).exists())
        self.assertEqual(Doctor.objects.get(id=self.doctor_pk).apellido, new_data)

    def test_modificar_ciudad_doctor(self):
        """La UpdateView debe modificar los datos de un doctor cualquiera"""
        nombre_new = self.fake.first_name()
        apellido_new = self.fake.last_name()
        ciudad_new = self.fake.city()
        data = {
            'apellido': apellido_new,
            'nombre': nombre_new,
            'ciudad': ciudad_new
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Doctor.objects.filter(id=self.doctor_pk).exists())
        self.assertEqual(Doctor.objects.get(id=self.doctor_pk).apellido, apellido_new)
        self.assertEqual(Doctor.objects.get(id=self.doctor_pk).nombre, nombre_new)
        self.assertEqual(Doctor.objects.get(id=self.doctor_pk).ciudad, ciudad_new)


class DoctorDeleteViewTests(TestCase):
    def setUp(self):
        self.fake = Faker('es_AR')

        # Creo instancias de Doctor
        self.cantidad_doctores_iniciales = 5
        for i in range(1,self.cantidad_doctores_iniciales+1):
            doctor = Doctor(
                id=i,
                apellido=self.fake.last_name(),
                nombre=self.fake.first_name(),
                ciudad=self.fake.city()
            )
            doctor.save()

        # Guardo la url
        self.doctor_pk = random.randint(1, self.cantidad_doctores_iniciales)
        self.url = reverse('doctor-delete-view',args=[self.doctor_pk])

    def test_doctor_confirm_delete_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'doctor_confirm_delete.html')

    def test_borrar_doctor(self):
        """La DeleteView debe borrar sin problemas un doctor existente"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Doctor.objects.count(),self.cantidad_doctores_iniciales-1)
        self.assertFalse(Doctor.objects.filter(id=self.doctor_pk).exists())

    def test_error_borrar_doctor_inexistente(self):
        """La DeleteVIew debe devolver error si el doctor que se desea borrar no existe"""
        response = self.client.post(reverse('doctor-delete-view',args=[7]))
        self.assertFalse(Doctor.objects.filter(id=7).exists())
        self.assertEqual(response.status_code, 404)


######################################
#### LENTES TEST
######################################
class LenteListViewTests(TestCase):
    def setUp(self):    
        self.url = reverse('lente-list-view')

    def test_lente_list_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lente_list.html')

    def test_lista_vacia_lente(self):
        """La ListView no debe devolver error cuando no existan lentes"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(),0)

    def test_listar_un_lente(self):
        """La LisView muestra el tipo de lente cargado"""
        lente = Lente(
            descripcion='CR39'
        )
        lente.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'],[lente])

    def test_listar_varios_doctores(self):
        """La ListView muestra los lentes cargadas"""
        lentes = []
        lentes_desc = ['CR39','MINERAL','BIO-VIS','FOTOCROMATICO']
        for idx, lente_desc in enumerate(lentes_desc):
            lente = Lente(
                id=idx+1,
                descripcion=lente_desc
            )
            lente.save()
            lentes.append(lente)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']),lentes)


class LenteCreateViewTests(TestCase):
    def setUp(self):
        self.url = reverse('lente-create-view')
        self.LENTES_DESC = ['CR39','MINERAL','BIO-VIS','FOTOCROMATICO']
        self.DESCRIPCION_LENTE_NUEVO = 'PROPIO'

    def test_lente_create_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lente_create_form.html')

    def test_crear_un_lente(self):
        """La CreateView crea un nuevo lente"""
        for idx, lente_desc in enumerate(self.LENTES_DESC):
            lente = Lente(
                id=idx+1,
                descripcion=lente_desc
            )
            lente.save()

        data = {
            'descripcion': self.DESCRIPCION_LENTE_NUEVO
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Lente.objects.count(),len(self.LENTES_DESC)+1)
        self.assertTrue(Lente.objects.filter(descripcion=self.DESCRIPCION_LENTE_NUEVO).exists())

    def test_crear_el_primer_lente(self):
        """La CreateView crea el primer lente de la base de datos"""
        data = {
            'descripcion': self.DESCRIPCION_LENTE_NUEVO
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(Lente.objects.count(),1)
        self.assertTrue(Lente.objects.filter(descripcion=self.DESCRIPCION_LENTE_NUEVO).exists())
        

class LenteUpdateViewTests(TestCase):
    def setUp(self):
        self.LENTES_DESC = ['CR39','MINERAL','BIO-VIS','FOTOCROMATICO']

        # Creo instancias de Lente
        for idx, lente_desc in enumerate(self.LENTES_DESC):
            lente = Lente(
                id=idx+1,
                descripcion=lente_desc
            )
            lente.save()

        # Guardo la url
        self.lente_pk = random.randint(1, len(self.LENTES_DESC))
        self.url = reverse('lente-update-view',args=[self.lente_pk])

    def test_lente_update_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lente_update_form.html')

    def test_modificar_descripcion_lente(self):
        """La UpdateView debe modificar la descripcion de un lente cualquiera"""
        new_data = 'PROPIO'
        data = {
            'descripcion': new_data
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Lente.objects.filter(id=self.lente_pk).exists())
        self.assertEqual(Lente.objects.get(id=self.lente_pk).descripcion, new_data)


class LenteDeleteViewTests(TestCase):
    def setUp(self):
        self.LENTES_DESC = ['CR39','MINERAL','BIO-VIS','FOTOCROMATICO']

        # Creo instancias de Lente
        for idx, lente_desc in enumerate(self.LENTES_DESC):
            lente = Lente(
                id=idx+1,
                descripcion=lente_desc
            )
            lente.save()

        # Guardo la url
        self.lente_pk = random.randint(1, len(self.LENTES_DESC))
        self.url = reverse('lente-delete-view',args=[self.lente_pk])

    def test_lente_confirm_delete_template(self):
        """El template del GET cargado es el esperado"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lente_confirm_delete.html')

    def test_borrar_lente(self):
        """La DeleteView debe borrar sin problemas un lente existente"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lente.objects.count(),len(self.LENTES_DESC)-1)
        self.assertFalse(Lente.objects.filter(id=self.lente_pk).exists())

    def test_error_borrar_doctor_inexistente(self):
        """La DeleteVIew debe devolver error si el lente que se desea borrar no existe"""
        response = self.client.post(reverse('lente-delete-view',args=[7]))
        self.assertFalse(Lente.objects.filter(id=7).exists())
        self.assertEqual(response.status_code, 404)

