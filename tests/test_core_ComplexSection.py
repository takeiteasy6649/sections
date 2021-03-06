import unittest

from sections.core import ComplexSection, SimpleSection, Dimensions, cached_property


class ComplexSectionTests(unittest.TestCase):
    
    def setUp(self):
        # Create a subclass of ComplexSection which suppresses
        # NotImplementedErrors

        class BasicImplementation(ComplexSection):
            sections  = []
            densities = []
            def update_sections(self):
                pass
        
        self.ComplexSection = BasicImplementation
        
    
    def test_set_dimensions_calls_update_sections(self):
        def error_raiser():
            raise ValueError
        section = self.ComplexSection()
        section.update_sections = error_raiser
        
        self.assertRaises(ValueError, section.set_dimensions)
    
    
    def test_initialization_of_sections(self):
        class Section(self.ComplexSection):
            sections  = [SimpleSection, SimpleSection]
            densities = NotImplemented
        section = Section()
        
        self.assertTrue(all(isinstance(s, SimpleSection) for s in section.sections))
    
    
    def test_initialization_of_densities(self):
        class Section1(self.ComplexSection):
            sections  = [SimpleSection, SimpleSection]
            densities = NotImplemented
        
        class Section2(self.ComplexSection):
            sections = [SimpleSection, SimpleSection]
            densities = [2, -3]
        
        class Section3(self.ComplexSection):
            sections = [SimpleSection, SimpleSection]
            densities = [2, 3, 4]

        section1 = Section1()
        section2 = Section2()
        
        self.assertEqual(len(section1.densities), len(section1.sections))
        self.assertEqual(section1.densities, [1.0,  1.0])
        self.assertTrue(all(isinstance(d, float) for d in section1.densities))

        self.assertEqual(section2.densities, [2.0, -3.0])
        self.assertTrue(all(isinstance(d, float) for d in section2.densities))
        
        # ValueError should be raised if number of densities and sections don't match
        self.assertRaises(ValueError, Section3)
        
    
    def test_density_propagates_to_subsections(self):
        class Section(self.ComplexSection):
            sections  = [SimpleSection, SimpleSection]
            densities = [2, -3]
        section = Section()
        
        self.assertEqual(section.sections[0].density,  2.0)
        self.assertEqual(section.sections[1].density, -3.0)
        
        section.set_density(-2)
        self.assertEqual(section.densities, [2.0, -3.0])
        self.assertEqual(section.sections[0].density, -4.0)
        self.assertEqual(section.sections[1].density,  6.0)


    def test_cached_properties(self):
        self.assertTrue(isinstance(ComplexSection._cog, cached_property))
        self.assertTrue(isinstance(ComplexSection.cog, cached_property))
        self.assertTrue(isinstance(ComplexSection.A, cached_property))
        self.assertTrue(isinstance(ComplexSection._I0, cached_property))
        self.assertTrue(isinstance(ComplexSection._I, cached_property))
        self.assertTrue(isinstance(ComplexSection.I0, cached_property))
        self.assertTrue(isinstance(ComplexSection.I, cached_property))
        

    def test_reset_cached_properties(self):
        # BaseSection.reset_cached_properties should be called when changing
        # dimensions, density or position
        
        # It should be also checked that cached properties are deleted by
        # reset_cached_properties. This is checked only for subclasses

        def error_raiser():
            raise ValueError
        section = self.ComplexSection()
        section.reset_cached_properties = error_raiser
    	
    	self.assertRaises(ValueError, section.set_dimensions)
    	self.assertRaises(ValueError, section.set_density, 2)
    	self.assertRaises(ValueError, section.set_position, 1, 2, 3)

